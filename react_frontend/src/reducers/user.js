const userReducer = (state = [], action) => {
	switch (action.type) {
		case 'SET_USER':
			return {
				user_token: action.payload
			}
		case 'UNSET_USER':
			return {}
		default: return state;
	}
}

export default userReducer;