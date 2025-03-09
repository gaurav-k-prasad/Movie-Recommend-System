import { Alert, Autocomplete, Box, Button, List, ListItem, TextField } from "@mui/material";
import { useEffect, useState } from "react";

const Body = () => {
	const [movieName, setMovieName] = useState("");
	const [movies, setMovies] = useState([]);
	const [recommendedMovies, setRecommendedMovies] = useState([]);
	const [query, setQuery] = useState("");
	const url = "https://movie-recommend-system-nx00.onrender.com";

	const handleFormSubmit = (event) => {
		event.preventDefault();
		fetch(`${url}/recommend?movie=${encodeURIComponent(query)}`)
			.then((response) => response.json())
			.then((data) => setRecommendedMovies(data))
			.catch((error) => console.error(error));
	};

	const handleInputChange = (event, value) => {
		setMovieName(value);
	};

	// Initial call on mount
	useEffect(() => {
		setQuery("a");
	}, []);

	// Debounce search query
	useEffect(() => {
		const timer = setTimeout(() => {
			if (movieName) setQuery(movieName);
		}, 500);

		return () => clearTimeout(timer);
	}, [movieName]);

	// Fetch movie data based on query
	useEffect(() => {
		if (query) {
			fetch(`${url}/get-movies?movie=${encodeURIComponent(query)}`)
				.then((response) => response.json())
				.then((data) => setMovies(data.map((movie, index) => ({ label: movie, id: index }))))
				.catch((error) => console.error(error));
		} else {
			setMovies([]);
		}
	}, [query]);

	const [alertOpen, setAlertOpen] = useState(true);

	return (
		<div className="w-full flex-1">
			<div className="w-1/2 m-auto">
				<form onSubmit={handleFormSubmit}>
					<br />
					{alertOpen && (
						<Alert
							severity="warning"
							onClose={() => {
								setAlertOpen(false);
							}}>
							Please wait about 1 minute if not working and try again. Server spins down due to
							inactivity
						</Alert>
					)}
					<Box>
						<div className="mt-10 flex gap-5 justify-center flex-col">
							<h1 className="text-3xl font-semibold text-purple-900">Search Movies</h1>
							<Autocomplete
								disablePortal
								options={movies}
								renderOption={(props, option) => (
									<li {...props} key={option.id}>
										{option.label}
									</li>
								)}
								renderInput={(params) => <TextField {...params} label="Movie" />}
								value={movieName}
								onInputChange={handleInputChange}
								fullWidth
							/>
							<Button variant="contained" type="submit">
								Recommend
							</Button>
						</div>
					</Box>

					<br />
					<br />

					<Box>
						<List>
							{recommendedMovies.map((data, i) => (
								<ListItem key={i} style={{ fontSize: "1.5rem" }}>
									{data[0]}
								</ListItem>
							))}
						</List>
					</Box>
				</form>
			</div>
		</div>
	);
};

export default Body;
