import React, { useState } from 'react'
import { useCookies } from 'react-cookie';
import './Profile.css';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

const Profile = () => {
    const [cookies, setCookie] = useCookies();

    const [profile, setProfile] = useState("");
    const url = "http://localhost:8000/profile/";
    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + cookies.jwt_token
        }
    })
        .then(response => response.json())
        .then(data => setProfile(data))
    return (
        <div class="profile">
            <h1>My information</h1>
            <Card sx={{ maxWidth: 345 }}>
                <CardContent>
                    <Typography gutterBottom variant="h5" component="div">
                        Username: {profile.username}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Email:{profile.email}
                    </Typography>

                    <Typography variant="body2" color="text.secondary">
                        Register_Date:{profile.register_date}
                    </Typography>

                </CardContent>

            </Card>
        </div>
    )
}

export default Profile
