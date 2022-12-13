/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ["./templates/**/*.html", "./static/src/**/*.js"],
	theme: {
		extend: {},
	},
	plugins: [],
};
// npx tailwindcss -i ./static/stylesheets/intw.css -o ./static/stylesheets/outtw.css --watch
// npx tailwindcss -i ./static/stylesheets/intw.css -o ./static/stylesheets/outtw.css
