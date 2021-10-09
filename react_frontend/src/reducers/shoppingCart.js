const initialState = {
	shopping_cart: []
}

const shoppingCart = (state = [], action) => {
	switch (action.type) {
		case 'ADD_TO_CART':
			return [...state, action.book];
		default: return state;
	}
}

export default shoppingCart;