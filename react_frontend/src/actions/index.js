
export const set_user = (user) => {
	return {
		type: 'SET_USER',
		payload: user
	};
};

export const unset_user = (user) => {
	return {
		type: 'UNSET_USER',
		payload: "TEST"
	}
}