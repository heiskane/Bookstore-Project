const initialState = {
	shopping_cart: []
}

const shoppingCart = (state = initialState, action) => {
	switch (action.type) {
		case 'ADD_TO_CART':
			return {
				...state,
				shopping_cart: [...state.shopping_cart, action.book],
			}
		default: return state;
	}
}

export default shoppingCart;