import { useEffect, useState } from 'react';
import { useParams } from "react-router-dom";
import { useCookies } from 'react-cookie';
//import { Document, Page } from 'react-pdf';
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack';
import axios from 'axios';

export default function ReadBook() {

	const [numPages, setNumPages] = useState(null);
	const [pageNumber, setPageNumber] = useState(1);
	const [book, setBook] = useState();
	const [uint8Book, setUint8Book] = useState();

	let { book_id } = useParams();
	const [cookies] = useCookies();

	function onDocumentLoadSuccess({ numPages }) {
	setNumPages(numPages);
	}

	// Similar to componentDidMount and componentDidUpdate:
	useEffect(() => {
		const instance = axios.create();
		instance.get('/books/' + book_id + '/download/', {
			responseType: 'blob',
			headers: {
				'authorization': 'Bearer ' + cookies.jwt_token
			}
		})
		.then((response) => {
			// https://developer.mozilla.org/en-US/docs/Web/API/Blob/arrayBuffer
			response.data.arrayBuffer()
				.then(buffer => setBook({data: new Uint8Array(buffer)}))
		})
	}, []);


	return (
		<div>
			<Document
				file={book}
				onLoadSuccess={onDocumentLoadSuccess}
			>
				<Page pageNumber={pageNumber} />
			</Document>
			<p>Page {pageNumber} of {numPages}</p>
		</div>
	)

}