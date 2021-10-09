import user_token from './user';
import shoppingCart from './shoppingCart';
import { combineReducers } from 'redux';

const allReducers = combineReducers({
	user_token: user_token,
	shopping_cart: shoppingCart
});

export default allReducers;