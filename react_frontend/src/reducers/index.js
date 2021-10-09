import user_token from './user';
import shoppingCart from './shoppingCart';
import { combineReducers } from 'redux';

const allReducers = combineReducers({
	user_token: user_token,
	shoppingCart: shoppingCart
});

export default allReducers;