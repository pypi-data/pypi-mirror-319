import math

from PepperPepper.environment import torch, nn, F

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride, downsample):
        super(ResidualBlock, self).__init__()
        self.body = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, stride, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_channels),
        )
        if downsample:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride, 0, bias=False),
                nn.BatchNorm2d(out_channels),
            )
        else:
            self.downsample = nn.Sequential()

    def forward(self, x):
        residual = x
        x = self.body(x)

        if self.downsample:
            residual = self.downsample(residual)
        out = F.leaky_relu(x+residual, 0.2, inplace=True)
        return out



class _FCNHead(torch.nn.Module):
    def __init__(self, in_channels, channels, norm_layer=torch.nn.BatchNorm2d):
        super(_FCNHead, self).__init__()
        self.block = torch.nn.Sequential()
        inter_channels = in_channels // 4
        self.block.append(torch.nn.Conv2d(in_channels=in_channels, out_channels=inter_channels, kernel_size=3, padding=1, bias=False))
        self.block.append(norm_layer(inter_channels))
        self.block.append(torch.nn.LeakyReLU(negative_slope=0.2))
        self.block.append(torch.nn.Dropout(0.1))
        self.block.append(torch.nn.Conv2d(in_channels=inter_channels, out_channels=channels, kernel_size=1))

    def forward(self, x):
        return self.block(x)



class patch_embed(nn.Module):
    def __init__(self, in_channels, out_channels, patch_size, V='V1'):
        super().__init__()
        self.in_channels = in_channels
        self.patch_size = patch_size
        self.V = V
        self.out_channels = out_channels

        if self.V == 'V1' and self.is_power_of_two(patch_size):
            self.block = self._make_patch_embed_V1(in_channels, out_channels, patch_size)
        else:
            self.block = self._make_patch_embed_last(in_channels, out_channels, patch_size)
            # raise ValueError(f"Unsupported version: {self.V}")



    def forward(self, x):
        y = self.block(x)
        return y

    def is_power_of_two(self, n):
        if n <= 1:
            return False
        log2_n = math.log2(n)
        return log2_n.is_integer()

    def check_divisible_by_power_of_two(self, n, k):
        divisor = 2 ** k

        if n % divisor != 0:
            raise ValueError(f"Error: {n} is not divisible by 2^{k}. Please try again.")

        return


    def _make_patch_embed_V1(self, in_channels, out_channels, patch_size):
        stage_num = int(math.log2(patch_size))

        # self.check_divisible_by_power_of_two(out_channels, stage_num)
        dim = out_channels // stage_num



        block = []
        for d in range(stage_num):
            block.append(nn.Sequential(
                nn.Conv2d(in_channels * (d + 1) if d == 0 else dim * (d), dim * (d + 1) if d+1 != stage_num else out_channels, kernel_size=2, stride=2),
                Permute(0, 2, 3, 1),
                nn.LayerNorm(dim * (d + 1) if d+1 != stage_num else out_channels),
                Permute(0, 3, 1, 2),
                (nn.GELU() if d+1 != 0 else nn.Identity())
            ))

        return nn.Sequential(*block)


    def _make_patch_embed_last(self, in_channels, channels, patch_size):
        # block = []

        block = nn.Sequential(
            nn.Conv2d(in_channels, channels // 2, kernel_size=patch_size,stride=patch_size),
            Permute(0, 2, 3, 1),
            nn.LayerNorm(channels // 2),
            Permute(0, 3, 1, 2),
            nn.GELU(),
            nn.Conv2d(channels//2, channels, kernel_size=1, stride=1),
            Permute(0, 2, 3, 1),
            nn.LayerNorm(channels // 2),
            Permute(0, 3, 1, 2)
        )


        return block






class Permute(nn.Module):
    def __init__(self, *args):
        super().__init__()
        self.args = args

    def forward(self, x: torch.Tensor):
        return x.permute(*self.args)
