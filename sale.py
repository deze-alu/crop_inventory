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
        return cls(
            row[0],
            row[1],
            row[2],
            row[3]
        )

    def __str__(self):
        return "{} | {} | {} | {}".format(
            self.sale_id,
            self.crop_id,
            self.quantity_sold,
            self.sale_date
        )
