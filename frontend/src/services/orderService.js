import api from "./api";

export const checkoutOrder = (payload) => {
    return api.post("payments/checkout_start/", payload);
};
