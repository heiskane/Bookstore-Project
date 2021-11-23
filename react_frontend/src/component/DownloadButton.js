import React from 'react';
import { useCookies } from 'react-cookie';
import Button from '@mui/material/Button';
import { download_book } from './DownloadFunc';


export default function BuyButton(props) {

	const [cookies] = useCookies();

	return (
		<Button
			variant="contained"
			onClick={() => {download_book(props.book_id, cookies.jwt_token)}}
		>Download</Button>
	)

}