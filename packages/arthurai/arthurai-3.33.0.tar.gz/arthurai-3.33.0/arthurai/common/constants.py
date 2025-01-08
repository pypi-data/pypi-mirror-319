API_PREFIX = "/api/v3"
API_PREFIX_V4 = "/api/v4"


class ListableStrEnum:
    """
    This class operates similar to Enum but passes mypy type checking.
    The members are accessed directly rather than by `.name` or `.value`.
    """

    @classmethod
    def list(cls):
        """
        Lists all attributes in alphabetical order
        """
        members = [
            getattr(cls, attr)
            for attr in dir(cls)
            if not callable(getattr(cls, attr)) and not attr.startswith("__")
        ]
        return sorted(members)


class InputType(ListableStrEnum):
    Tabular = "TABULAR"
    Image = "IMAGE"
    NLP = "NLP"
    TimeSeries = "TIME_SERIES"


class OutputType(ListableStrEnum):
    Regression = "REGRESSION"
    Multiclass = "MULTICLASS"
    Multilabel = "MULTILABEL"
    ObjectDetection = "OBJECT_DETECTION"
    TokenSequence = "TOKEN_SEQUENCE"
    RankedList = "RANKED_LIST"


class ValueType(ListableStrEnum):
    String = "STRING"
    Integer = "INTEGER"
    Float = "FLOAT"
    Image = "IMAGE"
    Boolean = "BOOLEAN"
    Timestamp = "TIMESTAMP"
    Unstructured_Text = (
        "UNSTRUCTURED_TEXT"  # don't remove old one, backward compatibility
    )
    BoundingBox = "BOUNDING_BOX"
    Tokens = "TOKENS"
    TokenLikelihoods = "TOKEN_LIKELIHOODS"
    RankedList = "RANKED_LIST"
    StringArray = "ARRAY(STRING)"
    TimeSeries = "TIME_SERIES"


class Stage(ListableStrEnum):
    ModelPipelineInput = "PIPELINE_INPUT"
    PredictFunctionInput = "PREDICT_FUNCTION_INPUT"
    PredictedValue = "PREDICTED_VALUE"
    NonInputData = "NON_INPUT_DATA"
    GroundTruth = "GROUND_TRUTH"
    GroundTruthClass = "GROUND_TRUTH_CLASS"


class TextDelimiter(ListableStrEnum):
    """This class contains patterns that can be used as text_delimiter for NLP models."""

    NOT_WORD = "\W+"
    """``"\W+"`` Splits on any character that is not a word.
    
    Ex: ``"this  is,aaaa,,,,,test!" = ["this", "is", "aaaa", "test", ""]``
    """

    WHITESPACE = "\s+"
    """``"\s+"`` Splits on whitespace.
    
    Ex: ``"this  is,a test! " = ["this", "is,a", "test!", ""]``"""

    COMMA = ","
    """``","`` Splits on a single comma.
    
    Ex: ``"this ,is,,a,test" = ["this ", "is", "", "a", "test"]``"""

    COMMA_PLUS = ",+"
    """``",+"`` Splits on one or more commas.
    
    Ex: ``"this ,is,,a,test" = ["this ", "is", "a", "test"]``"""

    PIPE = "\|"
    """``"\|"`` Splits on a single pipe.
    
    Ex: ``"this |is||a|test" = ["this ", "is", "", "a", "test"]``"""

    PIPE_PLUS = "\|+"
    """``"\|+"`` Splits on one or more pipes.
    
    Ex: ``"this |is||a|test" = ["this ", "is", "a", "test"]``"""


class Enrichment(ListableStrEnum):
    """This class contains constants for the names of enrichments"""

    AnomalyDetection = "anomaly_detection"
    BiasMitigation = "bias_mitigation"
    Explainability = "explainability"
    Hotspots = "hotspots"


class EnrichmentStatus(ListableStrEnum):
    """This class contains constants for the statuses of enrichments"""

    EnrichmentStatusDisabled = "Disabled"
    EnrichmentStatusPending = "Pending"
    EnrichmentStatusTraining = "Training"
    EnrichmentStatusReady = "Ready"
    EnrichmentStatusFailed = "Failed"


class ImageResponseType(ListableStrEnum):
    """Valid image response types supported by Arthur API"""

    RawImage = "raw_image"
    ResizedImage = "resized_image"
    Thumbnail = "thumbnail"
    LimeExplanation = "lime_explanation"


class ImageContentType(ListableStrEnum):
    """Valid image content types supported by Arthur API"""

    Png = "image/png"
    Jpeg = "image/jpeg"
    Gif = "image/gif"
    Tiff = "image/tiff"


IMAGE_FILE_EXTENSION_MAP = {
    ImageContentType.Png: ".png",
    ImageContentType.Jpeg: ".jpg",
    ImageContentType.Gif: ".gif",
    ImageContentType.Tiff: ".tff",
}


class AccuracyMetric(ListableStrEnum):
    Accuracy = "accuracy"
    Recall = "recall"
    F1 = "f1"
    Precision = "precision"


class Role(ListableStrEnum):
    User = "User"
    ModelOwner = "Model Owner"
    Administrator = "Administrator"


class ModelStatus(ListableStrEnum):
    Ready = "Ready"
    CreationFailed = "CreationFailed"
    Creating = "Creating"
    Pending = "Pending"
    Archived = "Archived"
    Archiving = "Archiving"
    ArchiveFailed = "ArchiveFailed"
    Unknown = "Unknown"


class InferenceType(ListableStrEnum):
    INFERENCE_DATA = "inference_data"
    REFERENCE_DATA = "reference_data"
    GROUND_TRUTH_DATA = "ground_truth_data"


class TimestampInferenceType(ListableStrEnum):
    INFERENCE_TIMESTAMP = "inference_timestamp"
    GROUND_TRUTH_TIMESTAMP = "ground_truth_timestamp"


ONBOARDING_SPINNER_MESSAGE = "Waiting for the model to be ready to accept inferences."
ONBOARDING_UPDATE_MESSAGE = (
    "We are still working on getting your model ready to accept inferences..."
)
DEFAULT_SERVICE_ACCOUNT = "default_sdk_service_account"

ENRICHMENTS_SPINNER_MESSAGE = (
    "Waiting for the model's enrichments to be ready to receive inferences."
)
ENRICHMENTS_UPDATE_MESSAGE = "We are still working on getting your model's enrichments ready to accept inferences..."
ENRICHMENT_READY_OR_FAILED_STATES = [
    EnrichmentStatus.EnrichmentStatusDisabled,
    EnrichmentStatus.EnrichmentStatusTraining,
    EnrichmentStatus.EnrichmentStatusReady,
    EnrichmentStatus.EnrichmentStatusFailed,
]

PARQUET_INGESTIBLE_INPUT_TYPES = [
    InputType.Tabular,
    InputType.Image,
    InputType.NLP,
]  # excludes TimeSeries
PARQUET_INGESTIBLE_OUTPUT_TYPES = [
    OutputType.Regression,
    OutputType.Multiclass,
    OutputType.Multilabel,
    OutputType.ObjectDetection,
    OutputType.TokenSequence,
]  # excludes RankedList
