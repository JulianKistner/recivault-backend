from typing import List

from fpdf import FPDF

from src.api.models.ingredients import IngredientReadInDB
from src.api.models.worksteps import WorkstepReadInDB



class ReceiptPDF(FPDF):
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(4)

    def chapter_description(self, description):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, description)
        self.ln()

    def chapter_ingredients(self, ingredients: List[IngredientReadInDB]):
        self.set_font('Arial', 'B', 12)
        self.multi_cell(0, 8, "Zutaten:")
        self.set_font('Arial', '', 12)
        for ingredient in ingredients:
            self.multi_cell(0, 6, f'     - {ingredient.amount} {ingredient.unit} \t {ingredient.ingredient}')
        self.ln()

    def chapter_worksteps(self, worksteps: List[WorkstepReadInDB]):
        self.set_font('Arial', 'B', 12)
        self.multi_cell(0, 8, "Arbeitsschritte:")
        self.set_font('Arial', '', 12)
        for workstep in worksteps:
            self.multi_cell(0, 6, f'{workstep.order_number}.) {workstep.workstep}')
        self.ln()