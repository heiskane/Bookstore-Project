
export const set_user = (user_token) => {
	return {
		type: 'SET_USER',
		user_token: user_token
	};
};

export const unset_user = (user_token) => {
	return {
		type: 'UNSET_USER'
	}
}

export const add_to_cart = (book) => {
	return {
		type: 'ADD_TO_CART',
		book: book
	}
}
