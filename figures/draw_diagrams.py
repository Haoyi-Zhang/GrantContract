"""Vector drawing primitives; copied into each independent project generator."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

plt.rcParams.update({'font.family':'STIXGeneral', 'mathtext.fontset':'stix',
                     'font.size':9, 'pdf.fonttype':42, 'ps.fonttype':42,
                     'text.usetex':False, 'axes.unicode_minus':False})
CM = 1 / 2.54

class Drawing:
    def __init__(self, bounds):
        x0,y0,x1,y1 = bounds
        self.fig = plt.figure(figsize=((x1-x0)*CM,(y1-y0)*CM))
        self.ax = self.fig.add_axes([0,0,1,1], xlim=(x0,x1), ylim=(y0,y1))
        self.ax.set_aspect('equal'); self.ax.axis('off')
        self.nodes = {}
        self.labels = []

    def text(self,x,y,label,size=9,ha='center',va='center'):
        artist=self.ax.text(x,y,label,fontsize=size,ha=ha,va=va,
                            linespacing=1.15,clip_on=False,zorder=4)
        self.labels.append([artist,None])
        return artist

    def box(self,name,x,y,w,h,label,dashed=False,shape='rect',size=9):
        style = {'edgecolor':'black','facecolor':'white','linewidth':.55,
                 'linestyle':(0,(4,3)) if dashed else 'solid', 'zorder':2}
        if shape == 'diamond':
            obj = Polygon([(x-w/2,y),(x,y+h/2),(x+w/2,y),(x,y-h/2)],**style)
        elif shape == 'circle': obj = Circle((x,y),w/2,**style)
        else: obj = Rectangle((x-w/2,y-h/2),w,h,**style)
        self.ax.add_patch(obj); self.text(x,y,label,size)
        self.labels[-1][1]=(x-w/2,y-h/2,x+w/2,y+h/2)
        self.nodes[name] = (x,y,w,h,shape)

    def point(self,name,side):
        x,y,w,h,_ = self.nodes[name]
        return {'n':(x,y+h/2),'s':(x,y-h/2),'e':(x+w/2,y),
                'w':(x-w/2,y),'nw':(x-w/2,y+h/2),
                'ne':(x+w/2,y+h/2),'c':(x,y)}[side]

    def line(self,points,dashed=False):
        xs,ys=zip(*points)
        self.ax.plot(xs,ys,color='black',linewidth=.55,
                     linestyle=(0,(4,3)) if dashed else 'solid',zorder=1)

    def arrow(self,p,q,dashed=False,via=()):
        points=[p,*via,q]
        if via:self.line(points[:-1],dashed)
        self.ax.add_patch(FancyArrowPatch(points[-2],points[-1],
                         arrowstyle='-|>',mutation_scale=7.5,linewidth=.55,
                         color='black',shrinkA=0,shrinkB=0,
                         linestyle=(0,(4,3)) if dashed else 'solid',zorder=1))

    def edge(self,a,b,sa='s',sb='n',**kwargs):
        self.arrow(self.point(a,sa),self.point(b,sb),**kwargs)

    def frame(self,x,y,w,h):
        self.ax.add_patch(Rectangle((x,y),w,h,fill=False,edgecolor='black',
                                   linewidth=.55,linestyle=(0,(4,3)),zorder=0))

    def save(self,out,name):
        # Fixed physical canvas: do not enlarge or rasterize the scientific figure.
        self.fig.canvas.draw()
        renderer=self.fig.canvas.get_renderer()
        x0,x1=self.ax.get_xlim();y0,y1=self.ax.get_ylim()
        for artist,node in self.labels:
            b=artist.get_window_extent(renderer).transformed(self.ax.transData.inverted())
            if b.x0<x0-.02 or b.x1>x1+.02 or b.y0<y0-.02 or b.y1>y1+.02:
                raise ValueError(name+': clipped label '+repr(artist.get_text()))
            if node and (b.x0<node[0]-.02 or b.x1>node[2]+.02 or b.y0<node[1]-.02 or b.y1>node[3]+.02):
                raise ValueError(name+': label exceeds node '+repr(artist.get_text()))
        self.fig.savefig(out/(name+'.pdf'),format='pdf',
                         metadata={'Creator':'Python Matplotlib','Producer':None,
                                   'CreationDate':None,'ModDate':None})
        plt.close(self.fig)

def render(out):
    d=Drawing((0,0,7.8,4.3))
    for name,x,y,label in [('a',1.8,3,r'$a:W_{\rm rlx}(x,1)$'),('b',1.8,1,r'$b:W_{\rm rel}(y,1)$'),('c',6,1,r'$c:R_{\rm acq}(y,1)$'),('d',6,3,r'$d:R_{\rm rlx}(x,0)$')]:
        d.box(name,x,y,2.8,.7,label,size=9)
    d.edge('a','b');d.edge('b','c','e','w');d.edge('c','d','n','s');d.edge('d','a','w','e',dashed=True)
    for x,y,label in [(1.35,2,r'$\mathsf{sb}$'),(3.9,.65,r'$\mathsf{rf},\mathsf{sw}$'),(6.45,2,r'$\mathsf{sb}$'),(3.9,3.45,r'$\mathsf{fr}$')]:d.text(x,y,label)
    d.save(out,'mp-cycle')
    d=Drawing((0,0,6.9,5.1))
    for i,word in enumerate(['00','01','10','11']):
        d.box(word,.9,4.4-i,.95,.6,'$'+word+'$',dashed=word=='10')
    d.box('z',5.1,3.9,2.8,1,r'$\phi=0$'+'\naccept')
    d.box('o',5.1,1.9,2.8,1,r'$\phi=1$'+'\nreject')
    for word in ['00','01']:d.edge(word,'z','e','w')
    for word in ['10','11']:d.edge(word,'o','e','w')
    d.text(3.3,.55,r'Words are $(\phi,d)$.'+'\nDashed box: forbidden completion.',size=8.5)
    d.save(out,'observation-fibers')
    d=Drawing((0,0,8.5,5.3))
    for n,x,y,w,label,dash in [('g0',2,4.5,2.8,'$p=0$ initially',False),('b0',6.25,4.5,2.8,'$p=1$ initially',False),('g1',2,2.8,3.6,r'$q_0=(1,1,0,0,0)$',False),('b1',6.25,2.8,3.6,r'$q_1=(1,1,0,1,0)$',True)]:
        d.box(n,x,y,w,.7,label,dashed=dash)
    d.edge('g0','g1');d.edge('b0','b1')
    d.text(.95,3.65,'flag; ack',size=8.5);d.text(7.25,3.65,'flag; ack',size=8.5)
    d.arrow((2,2.45),(2,1.3));d.arrow((6.25,2.45),(6.25,1.3))
    d.text(2,.85,'grant; read one',size=8.5)
    d.text(6.25,.85,'grant; hidden fill;\nread zero',size=8.5)
    # Zero count is stable, positive count can reinstall after grant.
    terminal=lambda pending,fill:0 if pending>0 and fill else 1
    if terminal(0,True)!=1 or terminal(1,True)!=0:raise ValueError('Receipt witness changed')
    d.save(out,'receipt-pair')

def main():
    import tempfile
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--check',action='store_true')
    a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True);render(a.output_dir)
    if a.check:
        with tempfile.TemporaryDirectory() as one,tempfile.TemporaryDirectory() as two:
            render(Path(one));render(Path(two))
            for name in ['mp-cycle','observation-fibers','receipt-pair']:
                if (Path(one)/(name+'.pdf')).read_bytes()!=(Path(two)/(name+'.pdf')).read_bytes():raise ValueError('Fresh exports differ: '+name)
    print('Three grant-contract vector figures and receipt witness checked.')

if __name__=='__main__':main()

