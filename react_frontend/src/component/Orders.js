import { useEffect, useState} from 'react'
import "./Orders.css"
import axios from "axios";
import { useCookies } from 'react-cookie';
import Box from '@mui/material/Box';
import Grid from "@mui/material/Grid";
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import OwnedBook from './OwnedBook';

const Orders = () => {

	const [cookies] = useCookies();
	const [books, setBooks] = useState();

	useEffect(() => {
		const instance = axios.create();
		instance.get("/profile/library", {
			headers: {
				'Authorization': 'Bearer ' + cookies.jwt_token
			}
		})
		.then((response) => {
			setBooks(response.data);
		})
		.catch(err => {
			return
		});
	}, []);

	if (!cookies.jwt_token) {
		return (
			<Alert severity="warning">
				<AlertTitle>Warning</AlertTitle>
				Please create and account and buy some books to fill your library 👍
			</Alert>
		)
	}

	if (!books) {
		return (
			<Alert severity="error">
				<AlertTitle>Error</AlertTitle>
				Something went horribly horribly wrong
			</Alert>
		)
	}

	return (
		<Box>
			<Grid
				container
				direction="row" 
				justifyContent="center"
				alignItems="baseline"
				spacing={2}
			>
				{books.map((book) => 
					<Grid item xs={2}>
						<OwnedBook key={book.title} book={book} />
					</Grid>
				)}
			</Grid>
		</Box>
	)
}

export default Orders
