import { Link } from 'react-router-dom';
import Button from '@mui/material/Button';

export default function ReadBookButton(props) {
	return (
      <Button
        variant="contained"
        component={Link}
        to={"/read_book/" + props.book_id}
      >
          Read
      </Button>
	)
}