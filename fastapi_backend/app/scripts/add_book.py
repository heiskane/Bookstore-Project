#!/usr/bin/env python

import base64 as b64
from datetime import date
from typing import List
from typing import Optional

import requests
import typer
from pydantic import BaseModel


def main(
    title: str = typer.Option(..., prompt=True),
    genres: str = typer.Option(..., prompt=True),
    authors: str = typer.Option(..., prompt=True),
    description: Optional[str] = typer.Option(None, prompt=True),
    language: Optional[str] = typer.Option(None),
    publication_date: str = typer.Option(..., prompt=True),
    isbn: Optional[str] = typer.Option(..., prompt=True, prompt_required=False),
    image_file_name: str = typer.Option(..., prompt=True),
    book_file_name: str = typer.Option(..., prompt=True)
    ) -> None:
    
    #typer.echo(book.json(exclude_unset=True, exclude_none=True))

    with open(image_file_name, "rb") as img:
        img_b64 = b64.b64encode(img.read())

    with open(book_file_name, "rb") as file:
        file_b64 = b64.b64encode(file.read())

    response = requests.post(
        "http://localhost:8000/books/",
        json={
          "authors": [author_name for author_name in authors.split(" ")],
          "genres": [{"name": genre_name} for genre_name in genres.split(" ")],
          "book": {
            "title": title,
            "description": description,
            "language": language,
            "publication_date": publication_date,
            "isbn": isbn,
            "image": img_b64,
            "file": file_b64
          }
        }
    )

    typer.echo(response)
    typer.echo(response.text)



if __name__ == "__main__":
    typer.run(main)