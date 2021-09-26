# Files

One of the critical components for the bookstore is going to be the ability to download files but from what I've learned from studying penetration testing this can easily become a big security flaw. With this in mind i took some time to think and research a good way of implementing this functianality without introducing any security flaws. Generally speaking user input should not be trusted and should be sanitized so i considered just using a few things for the filename like book ids, UUID strings, hashed book titles etc. Eventually i settled on a simple solution using a [function from werkzeug.utils](https://tedboy.github.io/flask/generated/werkzeug.secure_filename.html) then based my code on [this commend on github](https://github.com/tiangolo/fastapi/issues/426#issuecomment-542545608) and [the fastAPI documentation on file requests](https://fastapi.tiangolo.com/tutorial/request-files/)

* `main.py`:

```python

[...snip...]

# https://github.com/tiangolo/fastapi/issues/426#issuecomment-542545608
@app.post("/books/{book_id}/upload/")
async def upload_book_file(book_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
	if file.content_type != "application/pdf":
		raise HTTPException(status_code=400, detail="Only PDF allowed for now")
	# this results to something like "/home/user/bookstore_project/fastapi_backend/app/books/"
	# for docker deployment i would want it to be just /books
	upload_directory = getcwd() + "/app/books"
	book = crud.get_book(db = db, book_id = book_id)
	file_name = secure_filename(book.title + ".pdf")
	with open(path.join(upload_directory, file_name), 'wb') as upload_file:
		copyfileobj(file.file, upload_file)
	return {"filename": file_name}
```


To be able to download books i first wanted to be able to upload them. I set the endpoint as `/books/{book_id}/upload/` so that admin chooses the book that the file will be uploaded for. This means i can just fetch the title of the book from the database instead giving a user any more control than they need. From there I'm only allowing PDFs with that `if`-statement then just setting the upload directory to current working directory + `/app/books`. Now i finally taking the title of the book and sanitizing it with `secure_filename` function. This will change something like `../../../etc/passwd` to this `etc_passwd`. While this might not be the most fancy solution out there it is simple, working and should be a reasonable amount of security for the project. I also did look at [the source code for `secure_filename`](https://tedboy.github.io/flask/_modules/werkzeug/utils.html#secure_filename) and its only around 15 lines of code and im always happy to use a simple solution. Now the download feature isnt really too diffrent from the upload enpoint.

* `main.py`:

```python

[...snip...]

@app.get("/books/{book_id}/download/")
async def download_book(book_id: int, db: Session = Depends(get_db)):
	books_directory = getcwd() + "/app/books"
	book = crud.get_book(db = db, book_id = book_id)
	file_name = secure_filename(book.title + ".pdf")
	with open(path.join(books_directory, file_name), 'rb') as file:
		# https://stackoverflow.com/questions/60716529/download-file-using-fastapi
		return FileResponse(file.name, media_type='application/octet-stream',filename=file_name)
```

I guess the only noteworthy part about this is that im returning `FileResponse` object that i imported from `fastapi.responses`. Also notice that im not taking any filenames here. I am taking a book id and running the same `secure_filename` function on the title to get the correct filename. One drawback here is that when creating a book i am not uploading a file at the same time. This means it is possible to have a book with a file that actually contains the book. Ideally i would like to have a single endpoint do create the book and upload the file for it but according to [fastAPI documentation](https://fastapi.tiangolo.com/tutorial/request-files/#what-is-form-data) it is a limit of the HTTP protocol that you cant send form data and json. I do still feel like using something like `multipart/related` as the content type could allow this all of this in a single endpoint but that will be a task for another day. After all the admin that will be dealing with creating the books will either be me or the 2 other people working on this project.
