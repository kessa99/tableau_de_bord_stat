"""
analyse des données avec pandas
"""

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
            "total_etudiants": int(df["ID_étudiant"].nunique()),
            "total_notes": len(df),
            "moyenne": round(df["Note"].mean(), 2),
            "mediane": float(df["Note"].median()),
            "ecart_type": round(df["Note"].std(), 2),
            "taux_reussite_%": round((df["Note"] >= 10).mean() * 100, 2),
            "histogramme": np.histogram(df["Note"], bins=20, range=(0,20))[0].tolist(),
            "bins": np.histogram(df["Note"], bins=20, range=(0,20))[1].tolist(),
        }
    
    @staticmethod
    def stats_by_departement(csv_path: str) -> List[dict]:
        """
        calculer les statistiques par departement
        """
        df = pd.read_csv(csv_path)
        return(
            df.groupby(["Departement", "UE", "Matiere"])["Note"]
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
        df = dp.read_csv(csv_path)
        sub = df[df["Matiere"] == subject]
        if sub.empty:
            raise ValueError(f"Aucune note trouvée pour la matiere {subject}")
        return {
            "matiere": subject,
            "moyenne": round(sub["Note"].mean(), 2),
            "total_etudiants": int(sub["ID_étudiant"].nunique()),
            "total_notes": len(sub),
            "taux_reussite_%": round((sub["Note"] >= 10).mean() * 100, 2),
            "boxplot_data": sub["Note"].tolist(),
            "departement": sub["Departement"].unique().tolist(),
            "ue": sub["UE"].unique().tolist(),
            "mediane": float(sub["Note"].median()),
            "ecart_type": round(sub["Note"].std(), 2),
            "histogramme": np.histogram(sub["Note"], bins=20, range=(0,20))[0].tolist(),
            "bins": np.histogram(sub["Note"], bins=20, range=(0,20))[1].tolist(),
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
        return (sub.groupby("Matière")["Note"]
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

        bulletin = (sub.groupby(["Matière", "Enseignant"])["Note"]
                       .mean()
                       .round(2))

        # Classement par matière (optionnel mais très apprécié)
        classements = []
        for mat in sub["Matière"].unique():
            notes_matiere = df[df["Matière"] == mat]["Note"]
            note_etudiant = sub[sub["Matière"] == mat]["Note"].values[0]
            rang = (notes_matiere >= note_etudiant).sum()
            classements.append({
                "matiere": mat,
                "note": float(note_etudiant),
                "classement": f"{rang}e / {len(notes_matiere)}"
            })

        return {
            "etudiant_id": student_id,
            "moyenne": round(sub["Note"].mean(), 2),
            "credits_reussis": int((sub["Note"] >= 10).sum()),
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
            ranking = df.groupby("Matière")["Note"].mean().sort_values(ascending=False)
        else:
            ranking = df.groupby("Enseignant")["Note"].mean().sort_values(ascending=False)
        return ranking.head(10).to_dict()