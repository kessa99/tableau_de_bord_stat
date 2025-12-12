"""
Mapper pour le projet de nettoyage et analyse de données
"""

from clean_analyze.domain.entities.dataset_entity import DatasetEntity
from clean_analyze.models import Dataset

class DatasetMapper:
    """
    Mapper pour les entités Dataset
    """
    @staticmethod
    def to_entity(model: Dataset) -> DatasetEntity:
        """
        Map un modèle Dataset vers une entité DatasetEntity
        """
        return DatasetEntity(
            id=model.id,
            nom_fichier=model.nom_fichier,
            fichier_csv=model.fichier_csv.path if model.fichier_csv else None,
            data_upload=model.data_upload,
            stats_csv=model.stats_csv.path if model.stats_csv else None,
            notes_numpy=model.notes_numpy.path if model.notes_numpy else None
            )


# def map_dataset_entity_to_model(dataset_entity: DatasetEntity) -> Dataset:
#     """
#     Map une entité DatasetEntity vers un modèle Dataset
#     """
#     return Dataset(
#         id=dataset_entity.id,
#         nom_fichier=dataset_entity.nom_fichier,
#         fichier_csv=dataset_entity.fichier_csv,
#         data_upload=dataset_entity.data_upload,
#         stats_csv=dataset_entity.stats_csv,
#         notes_numpy=dataset_entity.notes_numpy)