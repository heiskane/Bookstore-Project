import axios from 'axios';
import fileDownload from 'js-file-download';


export function download_book(book_id, auth_token) {

	const instance = axios.create();

	instance.get('/books/' + book_id + '/download/', {
		responseType: 'blob',
		headers: {
			'authorization': 'Bearer ' + auth_token
		}
	})
	.then((response) => {
		// https://stackoverflow.com/questions/57607938/how-to-read-filename-from-response-reactjs
		const contentDisposition = response.headers['content-disposition']

		// https://stackoverflow.com/questions/23054475/javascript-regex-for-extracting-filename-from-content-disposition-header
		const filename = contentDisposition.match(
			/filename\*?=['"]?(?:UTF-\d['"]*)?([^;\r\n"']*)['"]?;?/
		)[1];

		fileDownload(response.data, filename);
	})
	.catch(err => {
		if (err.response && err.response.status === 403) {
			alert("You are not allowed to download this book")
		}
	})

}