import React from 'react';
import { useCookies } from 'react-cookie';
import axios from 'axios';
import fileDownload from 'js-file-download';
import Button from '@mui/material/Button';


export default function BuyButton(props) {

	const [cookies] = useCookies();
	
	function download_book() {
		const book_id = props.book_id;
		const instance = axios.create();
		instance.get('/books/' + book_id + '/download/', {
			responseType: 'blob',
			headers: {
				'authorization': 'Bearer ' + cookies.jwt_token
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

	return (
		<Button
			variant="contained"
			onClick={() => {download_book()}}
		>Download</Button>
	)

}