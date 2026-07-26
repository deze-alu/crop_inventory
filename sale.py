#!/usr/bin/python3
"""Defines the Sale class."""


class Sale:
    """Represents a crop sale."""

    def __init__(self, sale_id, crop_id, quantity_sold, sale_date):
        self.sale_id = sale_id
        self.crop_id = crop_id
        self.quantity_sold = quantity_sold
        self.sale_date = sale_date

    @classmethod
    def from_row(cls, row):
        """Creates a Sale object from a database row dictionary."""
        return cls(
            row["sale_id"],
            row["crop_id"],
            row["quantity_sold"],
            row["sale_date"]
        )

    def __str__(self):
        """Returns a readable string representation of the sale."""
        return "{} | {} | {} | {}".format(
            self.sale_id,
            self.crop_id,
            self.quantity_sold,
            self.sale_date
        )
