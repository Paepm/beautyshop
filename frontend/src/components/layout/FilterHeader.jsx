import { useNavigate, useSearchParams } from "react-router-dom";

function FilterHeader() {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const activeCategory = searchParams.get("category") || "";

    const categories = [
        'chairs', 'benches', 'cloth hanger', 'tables',
        'shelves', 'trash Cans', 'trolleys', 'other',
    ];

    const handleClick = (cat) => {
        const params = new URLSearchParams();
        if (cat) params.set("category", cat);
        navigate({ pathname: "/productlist", search: params.toString() });
    };

    return (
        <div className="bg-yellow-100 border-b border-yellow-300 px-4 py-2 flex flex-wrap justify-center gap-3">
            {/* ALL button zuerst */}
            <button
                onClick={() => handleClick("")}
                className={`px-4 py-1 rounded-full text-sm whitespace-nowrap transition-all`}
            >
                All
            </button>

            {/* KATEGORIEN */}
            {categories.map((cat) => (
                <button
                    key={cat}
                    onClick={() => handleClick(cat)}
                    className={`px-4 py-1 rounded-full text-sm whitespace-nowrap transition-all
                        ${activeCategory === cat ? "bg-black text-white" : "bg-white hover:bg-black hover:text-white"}`}
                >
                    {cat.charAt(0).toUpperCase() + cat.slice(1)}
                </button>
            ))}
        </div>
    );
}

export default FilterHeader;
