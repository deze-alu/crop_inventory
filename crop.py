class Crop:
    def __init__(self, crop_id, name, planting_date, harvest_date, status, quantity_planted):
        self.crop_id = crop_id
        self.name = name
        self.planting_date = planting_date
        self.harvest_date = harvest_date
        self.status = status
        self.quantity_planted = quantity_planted

    @classmethod
    def from_row(cls, row):
        return cls(
            row["crop_id"],
            row["name"],
            row["planting_date"] or "-",
            row["harvest_date"] or "-",
            row["status"] or "-",
            row["quantity_planted"] or 0,
        )

    def __str__(self):
        raise NotImplementedError(
            "Task B: return one tidy line for the inventory table. "
            "See docs/work-breakdown.md"
        )
