let select = document.getElementById("rsv_function");
let B = document.getElementById("B");
let K = document.getElementById("K");

select.onchange = (event) => {
	event.preventDefault();

	value = select.value;

	if (value == "bm25") {
		B.classList.remove("hidden");
		K.classList.remove("hidden");
	} else {
		B.classList.add("hidden");
		K.classList.add("hidden");
	}
};
