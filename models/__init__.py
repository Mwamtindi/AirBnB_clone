#!/usr/bin/python3
"""A file-based storage system for managing instances of various models"""
from models.engine.file_storage import FileStorage


fstorage = FileStorage()
fstorage.reload()
