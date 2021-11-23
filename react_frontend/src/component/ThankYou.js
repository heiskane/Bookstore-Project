import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

export default function ThankYou() {

  const user_token = useSelector(state => state.user_token)

  return (
    <Box
      display='flex'
      flexDirection='column'
      alignItems='center'
      justifyContent='center'
      padding='50px'
    >
      <Box
        display='flex'
        flexDirection='column'
        alignItems='center'
        justifyContent='center'
        maxWidth='50vw'
      >
        <Typography variant="h1">Thank You</Typography>
        <Typography>
          We thank you for shopping at HLG Books!
        </Typography>
        {user_token.sub ? (
          <Typography>
            You can navigate to the <Link to="/orders">My Books</Link> page
            to read or download your books.
          </Typography>
        ) : (
          <Typography>
            The purchased book should have downloaded automatically 
            in your browser. If this didnt happen please try selecting 
            the book you bought from the store and clicking on "Download".
            If this does not work please submit an issue on
            <Link
              to={{
                pathname: "https://github.com/heiskane/Bookstore-Project/issues"
              }}
              target="_blank"
            >
              our github page.
            </Link>
          </Typography>
        )}
      </Box>
    </Box>

  )

}