const shoppingCart = (state = [], action) => {
	switch (action.type) {
		case 'ADD_TO_CART':
			return [...state, action.book];
		case 'EMPTY_SHOPPINGCART':
			return [];
		default: return state;


	}
}


export default shoppingCart;
