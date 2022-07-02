from typing import Any


class Formatter:
    """
    This is the main function to format the line.

    Args:
        options: The options to format the line.
        others: Any args.

    Shape:
        XXXXXXXXX.

    Returns:
        Formatter object.

    Examples:
        .. code-block:: python

            # adaptive avg pool3d
            # suppose input data in shape of [N, C, D, H, W], `output_size` is [l, m, n],
            # output shape is [N, C, l, m, n], adaptive pool divide D, H and W dimensions
            # of input data into l * m * n grids averagely and performs poolings in each
            # grid to get output.
            # adaptive avg pool performs calculations as follow:
            #
            #     for i in range(l):
            #         for j in range(m):
            #             for k in range(n):
            #                 dstart = floor(i * D / l)
            #                 dend = ceil((i + 1) * D / l)
            #                 hstart = floor(j * H / m)
            #                 hend = ceil((j + 1) * H / m)
            #                 wstart = floor(k * W / n)
            #                 wend = ceil((k + 1) * W / n)
            #                 output[:, :, i, j, k] =
            #                     avg(input[:, :, dstart:dend, hstart: hend, wstart: wend])
            import paddle
            import numpy as np
            input_data = np.random.rand(2, 3, 8, 32, 32)
            x = paddle.to_tensor(input_data)
    """

    attr1: int
    attr2: str

    def __init__(self, options: dict[str, Any], others: Any):
        self.options = options

    def format_line(self) -> str:
        """
        This is the main function to format the line.

        Returns:
            str: The formatted line.
        """
        return ""

    # def format_file
