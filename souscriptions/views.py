from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch, cm
import json
from django.views.decorators.csrf import csrf_exempt
import locale
import os
from .models import SouscriptionEffectuee

# Create your views here.

@csrf_exempt
def generate_quittance_pdf(request, numero_transaction):
    try:
        # Récupérer la souscription depuis la base de données
        souscription = get_object_or_404(SouscriptionEffectuee, numero_transaction=numero_transaction)
        
        # Créer la réponse HTTP avec le type de contenu PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Recu_quittance_{numero_transaction}.pdf"'
        
        # Créer le document PDF
        doc = SimpleDocTemplate(
            response,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30,
            title=f"Reçu de quittance N°{numero_transaction} - SONATUR"
        )
        
        # Liste des éléments du PDF
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=12,
            alignment=1,  # Centre
            spaceAfter=20
        )
        
        header_style = ParagraphStyle(
            'HeaderStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=1,  # Centre
            spaceAfter=5
        )

        # Style des tableaux
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 0.39, 0.15)),  # Vert SONATUR
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 1), (-1, -1), 1, colors.black),  # Grille seulement à partir de la deuxième ligne
            ('BOX', (0, 0), (-1, -1), 1, colors.black),   # Bordure extérieure pour tout le tableau
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('WORDWRAP', (0, 0), (-1, -1), True),  # Activer le retour à la ligne automatique
            ('LEADING', (0, 0), (-1, -1), 12),     # Espacement des lignes
            ('SPAN', (0, 0), (1, 0)),  # Fusionner les cellules du titre
        ])
        
        # Style pour le tableau des banques (maintenant identique aux autres tableaux)
        bank_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 0.39, 0.15)),  # Vert SONATUR
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('WORDWRAP', (0, 0), (-1, -1), True),
            ('LEADING', (0, 0), (-1, -1), 12)
        ])

        # Ajuster les largeurs des colonnes
        col_widths = [
            doc.width*0.28,  # Première colonne un peu plus étroite
            doc.width*0.72   # Deuxième colonne plus large
        ]
        
        # Ajuster les largeurs des colonnes du tableau des banques pour qu'il prenne toute la largeur
        bank_col_widths = [
            doc.width*0.25,   # Nom
            doc.width*0.25,   # Code banque
            doc.width*0.25,   # Code guichet
            doc.width*0.25    # Numéro du compte
        ]

        # En-tête avec logos
        logo_path = "static/images/logo.png"
        qrcode_path = "static/images/qrcode.png"
      
        header_data = [
            [Image(logo_path, width=70, height=70), 
             [Paragraph("SONATUR", ParagraphStyle(
                 'HeaderTitle',
                 parent=styles['Heading1'],
                 fontSize=16,
                 alignment=1,
                 spaceAfter=5,
                 textColor=colors.darkgreen
             )),
              Paragraph("03 BP 7222 Ouagadougou 03 BURKINA FASO", header_style),
              Paragraph("Email: sonatur@fasonet.bf", header_style),
              Paragraph("Siège: +226 25 30 17 44 - Cellule Bobo: +226 20 97 01 41", header_style)],
             Image(qrcode_path, width=70, height=70)]
        ]
        header_table = Table(header_data, colWidths=[80, doc.width-160, 80])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 20))

        # Titre et numéro de quittance
        elements.append(Paragraph("Quittance de paiement", ParagraphStyle(
            'QuittanceTitle',
            parent=styles['Heading1'],
            fontSize=14,
            alignment=1,
            spaceAfter=5,
            textColor=colors.black
        )))
        elements.append(Paragraph(f"N° {souscription.numero_transaction}", ParagraphStyle(
            'QuittanceNumber',
            parent=styles['Normal'],
            fontSize=12,
            alignment=1,
            spaceAfter=5
        )))
        elements.append(Paragraph(f"Date: {souscription.date_souscription.strftime('%d/%m/%Y')}", ParagraphStyle(
            'QuittanceDate',
            parent=styles['Normal'],
            fontSize=11,
            alignment=1,
            spaceAfter=10
        )))

        # SITE SELECTIONNE
        site_data = [
            ["SITE SELECTIONNE", ""],
            ["Nom du site", str(souscription.operation.intitule)],
        ]
        site_table = Table(site_data, colWidths=col_widths)
        site_table.setStyle(table_style)
        elements.append(site_table)
        elements.append(Spacer(1, 10))

        # PARCELLE SELECTIONNEE
        parcelle_data = [
            ["PARCELLE SELECTIONNEE", ""],
            ["Type", str(souscription.type_parcelle)],
            ["Position", str(souscription.position)],
            ["Section", souscription.section],
            ["Lot", souscription.lot],
            ["Superficie total", f"{int(souscription.surface):,} m²".replace(',', ' ')],
            ["Coût unitaire", f"{int(souscription.cout_unitaire):,} FCFA/m²".replace(',', ' ')],
            ["Coût total", f"{int(souscription.prix_total):,} FCFA".replace(',', ' ')],
            ["Acompte minimal à payer", f"{int(souscription.acompte):,} FCFA".replace(',', ' ')]
        ]
        parcelle_table = Table(parcelle_data, colWidths=col_widths)
        parcelle_table.setStyle(table_style)
        elements.append(parcelle_table)
        elements.append(Spacer(1, 10))

        # INFORMATIONS DU SOUSCRIPTEUR
        if souscription.type_souscripteur.code == 'PHYSIQUE':
            souscripteur_data = [
                ["INFORMATIONS DU SOUSCRIPTEUR", ""],
                ["Nom", souscription.nom_complet],
                ["Date de naissance", souscription.date_naissance.strftime('%d/%m/%Y') if souscription.date_naissance else 'Non spécifié'],
                ["Lieu de naissance", souscription.lieu_naissance or 'Non spécifié'],
                ["Profession", souscription.profession or 'Non spécifié'],
                ["Genre", souscription.genre or 'Non spécifié'],
                ["Nationalité", souscription.pays or 'Non spécifié'],
                ["Type de document", souscription.document or 'Non spécifié'],
                ["Numéro de pièce", souscription.numero_piece or 'Non spécifié'],
                ["Date d'expiration", souscription.date_expiration.strftime('%d/%m/%Y') if souscription.date_expiration else 'Non spécifié'],
                ["Lieu d'établissement", souscription.lieu_etablissement or 'Non spécifié'],
                ["Téléphone", souscription.telephone],
                ["Email", souscription.email]
            ]
        else:
            souscripteur_data = [
                ["INFORMATIONS DU SOUSCRIPTEUR", ""],
                ["Raison sociale", souscription.raison_sociale],
                ["Forme juridique", souscription.forme_juridique],
                ["RCCM", souscription.rccm],
                ["IFU", souscription.ifu],
                ["Siège social", souscription.siege_social],
                ["Représentant", f"{souscription.nom_representant} {souscription.prenom_representant}".strip()],
                ["Fonction", souscription.fonction_representant],
                ["Téléphone", souscription.telephone],
                ["Email", souscription.email]
            ]
        souscripteur_table = Table(souscripteur_data, colWidths=col_widths)
        souscripteur_table.setStyle(table_style)
        elements.append(souscripteur_table)

        # Ajouter un saut de page avant la section PAIEMENT
        elements.append(PageBreak())

        # PAIEMENT
        paiement_data = [
            ["PAIEMENT", ""],
            ["Montant payé", f"{int(souscription.montant_souscription):,} FCFA".replace(',', ' ')],
            ["Méthode", souscription.methode_paiement],
            ["Date", souscription.date_paiement.strftime('%d/%m/%Y')],
            ["Numéro de transaction", souscription.numero_transaction]
        ]
        paiement_table = Table(paiement_data, colWidths=col_widths)
        paiement_table.setStyle(table_style)
        elements.append(paiement_table)
        elements.append(Spacer(1, 15))

        # INFORMATIONS IMPORTANTES
        info_data = [
            ["INFORMATIONS IMPORTANTES", ""],
            ["Délai de paiement", f"Vous disposez de {souscription.duree_depot_physique} jours ouvrables pour procéder au versement de l'acompte."],
            ["Compte bancaire", "Tout versement doit être effectué sur le compte SONATUR ci-dessous:"]
        ]
        info_table = Table(info_data, colWidths=col_widths)
        info_table.setStyle(table_style)
        elements.append(info_table)
        elements.append(Spacer(1, 15))

        # Tableau des banques
        bank_data = [["INFORMATIONS BANCAIRES DE LA SONATUR", "", "", ""]]  # Titre sur toute la largeur
        bank_data.append(["Nom", "Code banque", "Code guichet", "Numéro du compte"])  # En-têtes
        
        # Ajouter les comptes bancaires de la souscription
        for compte in souscription.comptes_bancaires.all():
            bank_data.append([
                compte.nom,
                compte.code_banque,
                compte.code_guichet,
                compte.numero_compte
            ])

        bank_table = Table(bank_data, colWidths=bank_col_widths)
        bank_table_style.add('SPAN', (0, 0), (-1, 0))  # Fusionner les cellules du titre
        bank_table.setStyle(bank_table_style)
        elements.append(bank_table)

        # Générer le PDF
        doc.build(elements)
        
        return response
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return HttpResponse(f"Erreur lors de la génération du PDF: {str(e)}", status=500)
