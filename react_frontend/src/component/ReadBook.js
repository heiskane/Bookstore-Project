import { useEffect, useState } from 'react';
import { useParams } from "react-router-dom";
import { useCookies } from 'react-cookie';
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack';
import axios from 'axios';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';

export default function ReadBook() {

	const [numPages, setNumPages] = useState(null);
	const [pageNumber, setPageNumber] = useState(1);
	const [book, setBook] = useState();

	let { book_id } = useParams();
	const [cookies] = useCookies();

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
		.catch((err) => {
			return
		})
	}, []);


	function onDocumentLoadSuccess({ numPages }) {
		setNumPages(numPages);
	}

	function nextPage() {
		if (pageNumber < numPages) {
			setPageNumber(pageNumber + 1)
		}
	}

	function previousPage() {
		if (pageNumber > 1) {
			setPageNumber(pageNumber - 1)
		}
	}

	if (!book) {
		return (
			<Alert severity="error">
				<AlertTitle>Error</AlertTitle>
				You probably dont own this book or my code broke
			</Alert>
		)
	}

	return (
		<Box
		  display="flex"
		  flexDirection="column" 
		  justifyContent="center"
		  alignItems="center"
		  minHeight="100vh"
		>
			<Document
				file={book}
				onLoadSuccess={onDocumentLoadSuccess}
			>
				<Page pageNumber={pageNumber} />
			</Document>
			<Box
			  display="flex"
			  flexDirection="row"
			>
				<Button variant="outlined" onClick={previousPage}>&lt;</Button>
				<Button variant="outlined" onClick={nextPage}>&gt;</Button>
			</Box>
			<p>Page {pageNumber} of {numPages}</p>
		</Box>
	)

}