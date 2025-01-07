import numpy as np
from papersize import parse_papersize
from tokenpdf.canvas import make_canvas
from tokenpdf.utils.verbose import vprint, vtqdm


class CanvasManager:
    """Manages canvas creation and token placement."""

    def __init__(self, config, loader, verbose):
        self.verbose = verbose
        self.print = vprint(verbose)
        self.tqdm = vtqdm(verbose)
        self.loader = loader
        self.canvas = make_canvas(config)
        self.config = config
        self.page_size, self.margin, self.page_size_margin = self._calculate_page_size()

    def place_tokens(self, tokens, layout):
        """Places tokens on the canvas."""
        verbose = self.verbose
        tqdm = vtqdm(verbose)
        print = vprint(verbose)
        sizes = [token.area(token_cfg, self.loader) for token, token_cfg in tqdm(tokens)]
        sizesm = [self._add_margin(size, token_cfg) for size, (_, token_cfg) in zip(sizes, tokens)]
        sizes_with_margins = [size for size, _ in sizesm]
        token_margins = [margin for _, margin in sizesm]

        print("Arranging tokens in pages")
        
        pages = layout.arrange(sizes_with_margins, self._gen_page_size(), verbose=verbose)
        canvas_pages = self._make_pages(pages)
        for placement_page, canvas_page in zip(tqdm(pages, desc="Drawing pages"),
                                                canvas_pages):
            for tindex, x, y, width, height in tqdm(placement_page, desc="Drawing tokens", leave=False):
                orig_size = sizes[tindex]
                tmargins = token_margins[tindex]
                if (width < height) != (orig_size[0] < orig_size[1]):
                    orig_size = orig_size[::-1]
                    tmargins = tmargins[::-1]

                xm, ym = np.array([x, y]) + self.margin + tmargins
                token, t_cfg = tokens[tindex]
                token.draw(canvas_page, t_cfg, self.loader, (xm, ym, *orig_size))

    def save(self):
        """Saves the canvas to a file."""
        self.canvas.save(verbose=self.verbose)

    def _calculate_page_size(self):
        config = self.config
        page_type = config.get('page_size', 'A4')
        page_size = np.array([float(m) for m in parse_papersize(page_type, "mm")])
        if config.get("orientation", "portrait").lower() in ["landscape", "l"]:
            page_size = page_size[::-1]
        margin_ratio = config.get("page_margin", config.get("margin", 0))
        margin = page_size * margin_ratio
        page_size_margin = page_size - 2 * margin
        return page_size, margin, page_size_margin


    def _gen_page_size(self):
        """ Generates pages (page sizes) as needed.
            Currently a constant stream of the same size """
        while True:
            yield self.page_size_margin

                
    def _make_pages(self, pages):
        return [self.canvas.create_page(self.page_size) for _ in pages]
    
    def _add_margin(self, size, token_cfg):
        margin = token_cfg.get("margin", 0) * np.array(size)
        return size + 2 * margin, margin