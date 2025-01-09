from typing import cast, Any
import pytest
from collections import namedtuple
import numpy as np
import sys
from unittest import mock



METHOD_NAME = "gaussian-splatting"


@pytest.fixture
def mock_gaussian_splatting(mock_torch, patch_modules):
    torch = mock_torch
    sys_modules = {
        "arguments": mock.MagicMock(),
        "gaussian_renderer": mock.MagicMock(),
        "scene": mock.MagicMock(),
        "scene.cameras": mock.MagicMock(),
        "scene.dataset_readers": mock.MagicMock(),
        "scene.gaussian_model": mock.MagicMock(),
        "utils": mock.MagicMock(),
        "utils.general_utils": mock.MagicMock(),
        "utils.image_utils": mock.MagicMock(),
        "utils.loss_utils": mock.MagicMock(),
        "utils.sh_utils": mock.MagicMock(),
        "utils.camera_utils": mock.MagicMock(),
        "utils.graphics_utils": mock.MagicMock(),
        "scipy": mock.MagicMock(),
    }
    # old_import = __import__
    # def _patch_import(name, globals=None, locals=None, fromlist=(), level=0):
    #     if level == 0 and name in sys_modules:
    #         return sys_modules[name]
    #     return old_import(name, globals, locals, fromlist, level)
    # with mock.patch("builtins.__import__", side_effect=_patch_import):
    with patch_modules(sys_modules):
        # from arguments import ModelParams, PipelineParams, OptimizationParams
        cast(mock.MagicMock, sys_modules["utils"]).camera_utils = sys_modules["utils.camera_utils"]
        cast(mock.MagicMock, sys_modules["utils.graphics_utils"]).fov2focal = lambda x, y: x / y
        arguments = cast(mock.MagicMock, sys_modules["arguments"])

        def setup_model_args(parser):
            parser.add_argument("--source_path")
            parser.add_argument("--sh_degree", default=3)
            parser.add_argument("--densify_until_iter", type=int, default=7)
            parser.add_argument("--densify_from_iter", type=int, default=1)
            parser.add_argument("--densify_grad_threshold", type=float, default=0.1)
            parser.add_argument("--densification_interval", type=int, default=2)
            parser.add_argument("--position_lr_max_steps", type=int, default=300)
            parser.add_argument("--opacity_reset_interval", type=int, default=2)
            parser.add_argument("--lambda_dssim", type=float, default=0.1)
            parser.add_argument("--white_background", action="store_true")
            parser.add_argument("--random_background", action="store_true")
            parser.add_argument("--resolution", type=int, default=None)
            parser.add_argument("--eval", action="store_true")
            out = mock.MagicMock()
            out.extract = lambda args: args
            return out

        arguments.ModelParams = setup_model_args

        def setup_opt_args(parser):
            parser.add_argument("--iterations", type=int, default=13)
            out = mock.MagicMock()
            out.extract = lambda args: args
            return out

        arguments.OptimizationParams = setup_opt_args

        def setup_pipe_args(parser):
            out = mock.MagicMock()
            out.extract = lambda args: args
            return out

        arguments.PipelineParams = setup_pipe_args

        def raise_error():
            raise NotImplementedError()

        cast(mock.MagicMock, sys_modules["scene"]).sceneLoadTypeCallbacks = sceneLoadTypeCallbacks = {
            "Colmap": raise_error,
        }

        class Camera:
            def __init__(self, **kwargs):
                self.image_width = kwargs["image"].shape[1]
                self.image_height = kwargs["image"].shape[0]
                self.original_image = kwargs["image"]
                self.znear = 0.1
                self.zfar = 100.0
                self.world_view_transform = torch.eye(4)
                for k, v in kwargs.items():
                    setattr(self, k, v)

        def loadCam(args, id, cam_info, resolution_scale):
            dct = cam_info._asdict()
            dct.pop("image_path")
            dct.pop("width")
            dct.pop("height")
            dct["FoVx"] = dct.pop("FovX")
            dct["FoVy"] = dct.pop("FovY")
            dct["image"] = torch.tensor(np.array(cam_info.image) / 255.0).permute(2, 0, 1).float()
            dct["colmap_id"] = 0
            dct["gt_alpha_mask"] = None
            dct["data_device"] = "cuda"
            Camera = sys_modules["scene.cameras"].Camera
            return Camera(**dct)

        def Scene(opt, gaussians, load_iteration):
            scene_info = cast(Any, sceneLoadTypeCallbacks["Colmap"]())
            scene = mock.MagicMock()
            scene.train_cameras = {1.0: scene_info.train_cameras}
        
            loadCam = sys_modules["utils.camera_utils"].loadCam
            scene.getTrainCameras = lambda: [loadCam(None, None, x, None) for x in scene_info.train_cameras]
            return scene

        cast(mock.MagicMock, sys_modules["scene"]).Scene = Scene

        def GaussianModel(*args, **kwargs):
            out = mock.MagicMock()
            out.capture.return_value = None
            return out

        cast(mock.MagicMock, sys_modules["scene"]).GaussianModel = GaussianModel
        cast(mock.MagicMock, sys_modules["scene.cameras"]).Camera = Camera
        cast(mock.MagicMock, sys_modules["utils.camera_utils"]).loadCam = loadCam
        cast(mock.MagicMock, sys_modules["scene.dataset_readers"]).CameraInfo = namedtuple("CameraInfo", ["uid", "R", "T", "FovY", "FovX", "image", "image_path", "image_name", "width", "height"])
        cast(mock.MagicMock, sys_modules["scene.dataset_readers"]).SceneInfo = namedtuple("SceneInfo", ["point_cloud", "train_cameras", "test_cameras", "nerf_normalization", "ply_path"])
        cast(mock.MagicMock, sys_modules["utils.loss_utils"]).l1_loss = lambda a, b: torch.abs(a - b).sum()
        cast(mock.MagicMock, sys_modules["utils.loss_utils"]).ssim = lambda a, b: torch.abs(a - b).sum()

        def render(viewpoint, gaussians, pipe, background):
            shape = viewpoint.image.shape
            return dict(
                render=torch.zeros(shape, dtype=torch.float32),
                viewspace_points=torch.zeros((124, 2), dtype=torch.float32),
                visibility_filter=torch.zeros((124, 2), dtype=bool),
                radii=torch.zeros((124, 2), dtype=torch.float32),
            )

        cast(mock.MagicMock, sys_modules["gaussian_renderer"]).render = render
        yield None
        sys_modules.pop("nerfbaselines.methods.gaussian_splatting", None)


@pytest.mark.method(METHOD_NAME)
def test_train_gaussian_splatting_mocked(mock_gaussian_splatting, run_test_train):
    run_test_train()


@pytest.mark.method(METHOD_NAME)
@pytest.mark.apptainer
def test_train_gaussian_splatting_apptainer(run_test_train):
    run_test_train()


@pytest.mark.method(METHOD_NAME)
@pytest.mark.docker
def test_train_gaussian_splatting_docker(run_test_train):
    run_test_train()


@pytest.mark.method(METHOD_NAME)
@pytest.mark.conda
def test_train_gaussian_splatting_conda(run_test_train):
    run_test_train()

