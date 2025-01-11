from etna import SETTINGS

if SETTINGS.torch_required:
    from etna.models.nn.deepar import DeepARModel
    from etna.models.nn.deepar_native import DeepARNativeModel
    from etna.models.nn.deepstate.deepstate import DeepStateModel
    from etna.models.nn.mlp import MLPModel
    from etna.models.nn.nbeats import NBeatsGenericModel
    from etna.models.nn.nbeats import NBeatsInterpretableModel
    from etna.models.nn.patchts import PatchTSModel
    from etna.models.nn.rnn import RNNModel
    from etna.models.nn.tft import TFTModel
    from etna.models.nn.tft_native import TFTNativeModel
    from etna.models.nn.utils import PytorchForecastingDatasetBuilder

if SETTINGS.chronos_required:
    from etna.models.nn.chronos import ChronosBoltModel
    from etna.models.nn.chronos import ChronosModel

if SETTINGS.timesfm_required:
    from etna.models.nn.timesfm import TimesFMModel
