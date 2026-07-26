#!/usr/bin/python3
"""Defines the Crop class."""


class Crop:
    """Represents a crop in the inventory system."""

    def __init__(self, crop_id, name, planting_date, harvest_date,
                 status, quantity_planted):
        self.crop_id = crop_id
        self.name = name
        self.planting_date = planting_date
        self.harvest_date = harvest_date
        self.status = status
        self.quantity_planted = quantity_planted

    @classmethod
    def from_row(cls, row):
        """Creates a Crop object from a database row dictionary."""
        return cls(
            row["crop_id"],
            row["name"],
            row["planting_date"],
            row["harvest_date"],
            row["status"],
            row["quantity_planted"]
        )

    def __str__(self):
        """Returns a readable string representation of the crop."""
        return "{} | {} | {} | {} | {} | {}".format(
            self.crop_id,
            self.name,
            self.planting_date,
            self.harvest_date,
            self.status,
            self.quantity_planted
        )
