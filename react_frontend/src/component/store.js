import { configureStore } from "@reduxjs/toolkit";
import { bookstoreReducer } from './slice';
export const store = configureStore({
    reducer: {
        bookstore: {}
    },
})