"""
analyse des données avec pandas
"""

from typing import List, Dict, Any
import pandas as pd
import numpy as np

class PandaAnalysisEngine:
    """
    Analyse des données avec pandas
    """

    @staticmethod
    def load_df(csv_path: str) -> pd.DataFrame:
        """
        charger un dataframe depuis un fichier csv
        """
        return pd.read_csv(csv_path)
    
    @staticmethod
    def global_stats(csv_path: str) -> dict:
        """
        calculer les statistiques globales du dataframe
        """
        df = pd.read_csv(csv_path)
        return {
            "total_etudiants": int(df["student_id"].nunique()),
            "total_notes": len(df),
            "moyenne": round(df["note"].mean(), 2),
            "mediane": float(df["note"].median()),
            "ecart_type": round(df["note"].std(), 2),
            "taux_reussite_%": round((df["note"] >= 10).mean() * 100, 2),
            "histogramme": np.histogram(df["note"], bins=20, range=(0,20))[0].tolist(),
            "bins": np.histogram(df["note"], bins=20, range=(0,20))[1].tolist(),
        }
    
    @staticmethod
    def stats_by_departement(csv_path: str) -> List[dict]:
        """
        calculer les statistiques par departement
        """
        df = pd.read_csv(csv_path)
        return(
            df.groupby(["departement", "Code_ue", "Matiere"])["note"]
            .agg(
                moyenne="mean",
                mediane="median",
                ecart_type="std",
                nb_etudiants="nunique",
                taux_reussite=lambda x: round((x>=10).mean() * 100, 2),
                count="count",
            )
            .round()
            .reset_index()
            .sort_values(by="moyenne", ascending=False)
            .to_dict(orient="records")
        )
    
    @staticmethod
    def stats_by_matiere(csv_path: str, subject: str) -> dict:
        """
        calculer les statistiques par matiere
        """
        df = pd.read_csv(csv_path)
        sub = df[df["Matiere"] == subject]
        if sub.empty:
            raise ValueError(f"Aucune note trouvée pour la matiere {subject}")
        return {
            "matiere": subject,
            "moyenne": round(sub["note"].mean(), 2),
            "total_etudiants": int(sub["ID_étudiant"].nunique()),
            "total_notes": len(sub),
            "taux_reussite_%": round((sub["note"] >= 10).mean() * 100, 2),
            "boxplot_data": sub["note"].tolist(),
            "departement": sub["departement"].unique().tolist(),
            "code_ue": sub["Code_ue"].unique().tolist(),
            "mediane": float(sub["note"].median()),
            "ecart_type": round(sub["note"].std(), 2),
            "histogramme": np.histogram(sub["note"], bins=20, range=(0,20))[0].tolist(),
            "bins": np.histogram(sub["note"], bins=20, range=(0,20))[1].tolist(),
        }
    
    @staticmethod
    def stats_by_teacher(csv_path: str, teacher: str) -> List[Dict]:
        """
        calculer les statistiques par enseignant
        """
        df = pd.read_csv(csv_path)
        sub = df[df["Enseignant"].str.contains(teacher, case=False, na=False)]
        if sub.empty:
            raise ValueError("Enseignant non trouvé")
        return (sub.groupby("Matière")["note"]
                   .agg(moyenne="mean", nb_etudiants="count")
                   .round(2)
                   .sort_values("moyenne", ascending=False)
                   .reset_index()
                   .to_dict(orient="records"))

    @staticmethod
    def student_report(csv_path: str, student_id: str) -> Dict[str, Any]:
        """
        calculer les statistiques par étudiant
        """
        df = pd.read_csv(csv_path)
        sub = df[df["ID_étudiant"] == student_id]
        if sub.empty:
            raise ValueError("Étudiant non trouvé")

        bulletin = (sub.groupby(["Matière", "Enseignant"])["note"]
                       .mean()
                       .round(2))

        # Classement par matière (optionnel mais très apprécié)
        classements = []
        for mat in sub["Matière"].unique():
            notes_matiere = df[df["Matière"] == mat]["note"]
            note_etudiant = sub[sub["Matière"] == mat]["note"].values[0]
            rang = (notes_matiere >= note_etudiant).sum()
            classements.append({
                "matiere": mat,
                "note": float(note_etudiant),
                "classement": f"{rang}e / {len(notes_matiere)}"
            })

        return {
            "etudiant_id": student_id,
            "moyenne": round(sub["note"].mean(), 2),
            "credits_reussis": int((sub["note"] >= 10).sum()),
            "bulletin": bulletin.to_dict(),
            "classements": classements
        }

    @staticmethod
    def top_flops(csv_path: str, category: str = "matiere") -> Dict:
        """
        calculer les top 10 flops
        """
        df = pd.read_csv(csv_path)
        if category == "matiere":
            ranking = df.groupby("Matière")["note"].mean().sort_values(ascending=False)
        else:
            ranking = df.groupby("Enseignant")["note"].mean().sort_values(ascending=False)
        return ranking.head(10).to_dict()