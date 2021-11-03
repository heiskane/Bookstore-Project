const shoppingCart = (state = [], action) => {
	switch (action.type) {
		case 'ADD_TO_CART':
			return [...state, action.book];
		case 'EMPTY_SHOPPINGCART':
			return [];
		case 'REMOVE_FROM_SHOPPINGCART':
			let newShoppingCart = [...state];
			const index = state.findIndex((cartItem) => cartItem.id === action.id);

			if (index >= 0) {
				//item exists in basket, remove it...
				newShoppingCart.splice(index, 1);
			} else {
				console.warn(
					`Can't remove product (id: ${action.id}) as it's empty `
				)
			}
			return newShoppingCart;
		default: return state;


	}
}


export default shoppingCart;
