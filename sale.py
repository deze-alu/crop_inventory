class Sale:
    def __init__(self, sale_id, crop_id, quantity_sold, sale_date):
        self.sale_id = sale_id
        self.crop_id = crop_id
        self.quantity_sold = quantity_sold
        self.sale_date = sale_date

    @classmethod
    def from_row(cls, row):
        return cls(
            row["sale_id"],
            row["crop_id"],
            row["quantity_sold"],
            row["sale_date"] or "-",
        )

    def __str__(self):
        raise NotImplementedError(
            "Task B: return one tidy line for the sales table. "
            "See docs/work-breakdown.md"
        )
