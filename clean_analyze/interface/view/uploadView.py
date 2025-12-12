"""
vue pour uploader les datasets
"""

from django.views.decorators.csrf import csrf_exempt

from clean_analyze.domain.useCase.upload_dataset import UploadDatasetUseCase
from clean_analyze.infrastucture.repositories.dataset_repo import DjangoDatasetRepository
from clean_analyze.interface.utils import standard_response

@csrf_exempt
def upload_dataset(request):
    """
    Uploader un fichier CSV et le sauvegarder dans le système.
    Ce use case ne fait PAS d'analyse ici (l'analyse se fait dans un autre use case séparé).
    """
    if request.method != "POST" or not request.FILES.get("file"):
        return standard_response(
            message="Veuillez envoyer un fichier CSV",
            status_str="failed"
        )
    
    file = request.FILES["file"]

    dataset_repository = DjangoDatasetRepository()
    use_case = UploadDatasetUseCase(dataset_repository)
    try:
        dataset = use_case.execute(file.name, file.path)

        return standard_response(
            message="Fichier uploadé avec succès",
            content={
                "dataset_id": str(dataset.id)
            },
            code=201,
            status_str="succes"
        )
    except Exception as e:
        return standard_response(
            message=str(e),
            content={},
            status_str="failed",
            code=500
        )
    