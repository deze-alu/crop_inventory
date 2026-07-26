#!/usr/bin/python3
"""Defines the Crop class."""


class Crop:
    """Represents a crop in the inventory."""

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
        return cls(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        )

    def __str__(self):
        return "{} | {} | {} | {} | {} | {}".format(
            self.crop_id,
            self.name,
            self.planting_date,
            self.harvest_date,
            self.status,
            self.quantity_planted
        )
