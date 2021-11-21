function getToken(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getToken("csrftoken");

console.log(csrftoken);

axios.defaults.headers.common["X-CSRFTOKEN"] = csrftoken;
axios.defaults.headers.common["Content-Type"] = "application/json";

const app = {
  el: "#ebuy",
  delimiters: ["[[", "]]"],
  data() {
    return {
      num: 0,
      name: "",
      email: "",
      address: "",
      city: "",
      region: "",
      country: "",
    };
  },
  computed: {
    isLogined() {
      if (user === "AnonymousUser") {
        return false;
      } else {
        return true;
      }
    },
  },
  mounted() {
    this.getCardItems();
  },
  methods: {
    getCardItems() {
      if (this.isLogined) {
        axios
          .get("/card_items")
          .then((data) => (this.num = data.data.itemsTotal));
      }
    },
    addCartItem(e) {
      productId = e.target.dataset.product;
      action = e.target.dataset.action;
      data = { productId: productId, action: action };
      axios
        .post("/update_item/", data)
        .then((data) => {
          this.num = data.data.itemsTotal;
          location.reload();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    checkout() {
      if (this.isLogined) {
        data = {
          address: this.address,
          city: this.city,
          region: this.region,
          country: this.country,
        };
      }
      axios
        .post("/checkout_proceed/", data)
        .then((data) => {
          if (data.data.status == "Okay") {
            alert("Order Successfully placed");
            location.href = "/";
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};

const cart = new Vue(app);
