from server.models.PaddleSeg.Matting.deploy.python.infer import Predictor


class PredictParam:
    cfg = None
    device = "cpu"
    save_dir = "./"
    print_detail = True
    enable_mkldnn = False
    cpu_threads = 10
    batch_size = 1
    benchmark = False
    fg_estimate = True

    def __init__(self, cfg=None, device="cpu", save_dir="./", print_detail=True, enable_mkldnn=False, cpu_threads=10,
                 batch_size=1, benchmark=False, fg_estimate=True):
        self.cfg = cfg
        self.device = device
        self.save_dir = save_dir
        self.print_detail = print_detail
        self.enable_mkldnn = enable_mkldnn
        self.cpu_threads = cpu_threads
        self.batch_size = batch_size
        self.benchmark = benchmark
        self.fg_estimate = fg_estimate


def get_predictor():
    fast_args = PredictParam(cfg="/Users/nickname4th/nicktool/server/models/PaddleSeg/Matting/modnet-mobilenetv2/deploy.yaml",
                             save_dir="/Users/nickname4th/nicktool/server/models/output/results", print_detail=False)
    slow_args = PredictParam(cfg="/Users/nickname4th/nicktool/server/models/PaddleSeg/Matting/modnet-resnet50_vd/deploy.yaml",
                             save_dir="/Users/nickname4th/nicktool/server/models/output/results", print_detail=False)
    fast_predictor = Predictor(fast_args)
    slow_predictor = Predictor(slow_args)
    return fast_predictor, slow_predictor


def test():
    fast, slow = get_predictor()
    fast.run(
        ["/Users/nickname4th/nicktool/server/models/PaddleSeg/Matting/data/PPM-100/val/fg/test.jpg"])
