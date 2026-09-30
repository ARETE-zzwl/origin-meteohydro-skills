"""Make offline, SYNTHETIC Matplotlib teaching examples, not research results."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, TwoSlopeNorm
from matplotlib.ticker import NullLocator
import numpy as np

from palette_tools import catalog, load_palette, mpl_cmap


def save(fig, path):
    fig.savefig(path.with_suffix('.png'), dpi=170, facecolor='white')
    fig.savefig(path.with_suffix('.pdf'), facecolor='white')
    plt.close(fig)


def atlas(out):
    entries = catalog()['palettes']
    fig, axes = plt.subplots(len(entries), 1, figsize=(12, 15))
    for ax, entry in zip(axes, entries):
        rgb = load_palette(entry['name'])[1]
        ax.imshow(rgb[None, :, :] / 255, aspect='auto', interpolation='nearest')
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_ylabel(entry['name'], rotation=0, ha='right', va='center', fontsize=9)
        ax.text(1.015, .5, entry['kind'], transform=ax.transAxes, va='center', fontsize=8, color='#59626B')
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.subplots_adjust(left=.28, right=.86, top=.93, bottom=.055, hspace=.65)
    fig.suptitle('METEOROLOGY + HYDROLOGY\nOffline scientific palette library', x=.08, ha='left', fontsize=19)
    fig.text(.08, .017, '25 palettes | RGB / HEX / JASC PAL | Colors do not encode units, bounds or missing values.\n'
             'Matplotlib / cmocean / Scientific Colour Maps / NCAR NCL / local roles', fontsize=9, color='#59626B')
    save(fig, out / 'palette_atlas')


def gallery(out):
    rng = np.random.default_rng(20260929)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.spines.top': False,
                         'axes.spines.right': False, 'axes.titleweight': 'bold', 'axes.linewidth': .65,
                         'savefig.facecolor': 'white', 'pdf.fonttype': 42})
    fig, axes = plt.subplots(4, 3, figsize=(15, 16), layout='constrained')
    titles = ['Anomaly + circulation', 'Discrete precipitation', 'Vertical section',
              'Hovmoller diagram', 'Event-relative composite', 'Effect + interval',
              'Rainfall and runoff', 'Flow-duration curve', 'Observed vs simulated',
              'Probability reliability', 'EOF-like pattern + coefficient', 'Directional frequency']
    for i, (ax, title) in enumerate(zip(axes.flat, titles)):
        ax.set_title(f'{chr(97+i)}  {title}', loc='left', fontsize=11, pad=10)
    lon = np.linspace(105, 130, 45)
    lat = np.linspace(18, 43, 40)
    xx, yy = np.meshgrid(lon, lat)
    anomaly = 2 * np.sin((xx-113)/5) * np.cos((yy-30)/7)
    ax = axes[0, 0]
    im = ax.pcolormesh(xx, yy, anomaly, cmap=mpl_cmap('RdBu_r'), norm=TwoSlopeNorm(0, -2, 2), shading='auto')
    q = ax.quiver(xx[::6, ::6], yy[::6, ::6], np.cos(yy[::6, ::6]/6)*3,
                  np.sin(xx[::6, ::6]/8)*3, color='#293744', scale=38, width=.003)
    ax.quiverkey(q, .84, 1.025, 3, '3 m s$^{-1}$', labelpos='W')
    ax.set(xlabel='Longitude (degrees E)', ylabel='Latitude (degrees N)')
    fig.colorbar(im, ax=ax, label='Temperature anomaly (K)', shrink=.85)
    ax.text(.02, .03, 'Coordinate demo; no geographic basemap', transform=ax.transAxes, fontsize=7)
    ax = axes[0, 1]
    rain = np.exp(-((xx-119)**2+(yy-29)**2)/30)*110
    levels = [0, 1, 5, 10, 25, 50, 100, 150]
    cmap = mpl_cmap('cmocean_rain')
    im = ax.pcolormesh(xx, yy, rain, cmap=cmap, norm=BoundaryNorm(levels, cmap.N), shading='auto')
    fig.colorbar(im, ax=ax, ticks=levels, label='Rainfall (mm day$^{-1}$)', shrink=.85)
    ax.set(xlabel='Longitude (degrees E)', ylabel='Latitude (degrees N)')
    ax = axes[0, 2]
    pressure = np.geomspace(1000, 100, 35)
    field = np.sin((lat[None, :]-25)/9) * np.cos(np.log(pressure[:, None]/450))*4
    im = ax.contourf(lat, pressure, field, levels=np.linspace(-4, 4, 17), cmap=mpl_cmap('vik'))
    ax.set_yscale('log')
    ax.set(ylim=(1000, 100), xlabel='Latitude (degrees N)', ylabel='Pressure (hPa)')
    ax.set_yticks([1000, 850, 500, 300, 200, 100], ['1000', '850', '500', '300', '200', '100'])
    ax.yaxis.set_minor_locator(NullLocator())
    fig.colorbar(im, ax=ax, label='Wind anomaly (m s$^{-1}$)', shrink=.85)
    ax = axes[1, 0]
    days = np.arange(-10, 11)
    wave = np.sin((lon[None, :]-115)/5-days[:, None]/4)
    im = ax.pcolormesh(lon, days, wave, shading='auto', cmap=mpl_cmap('cmocean_balance'), vmin=-1, vmax=1)
    ax.set(xlabel='Longitude (degrees E)', ylabel='Relative day')
    fig.colorbar(im, ax=ax, label='Standardized anomaly', shrink=.85)
    ax = axes[1, 1]
    line = 1.7*np.exp(-((days-1)/4)**2)-.45
    ax.fill_between(days, line-.25, line+.25, color='#296795', alpha=.18, label='Illustrative band')
    ax.plot(days, line, color='#296795', label='Synthetic composite')
    ax.axhline(0, color='.65', lw=.7)
    ax.axvline(0, color='.5', ls='--', lw=.8)
    ax.set(xlabel='Days from anchor', ylabel='Standardized anomaly')
    ax.legend(frameon=False, fontsize=7, loc='upper left')
    ax = axes[1, 2]
    y = np.arange(4)
    est = np.array([.4, .7, -.2, .3])
    ax.errorbar(est, y, xerr=[[.2, .3, .25, .2], [.3, .2, .4, .35]], fmt='o',
                color='#296795', capsize=3, lw=1.2)
    ax.axvline(0, color='.6', lw=.8)
    ax.set(yticks=y, yticklabels=['Group A', 'Group B', 'Group C', 'Group D'],
           ylim=(-.35, 3.65), xlabel='Effect (example units)')
    ax.text(.02, .96, 'Illustrative intervals, not inference', transform=ax.transAxes, va='top', fontsize=7)
    ax = axes[2, 0]
    t = np.arange(20)
    precip = 25*np.exp(-((t-5)/1.5)**2)
    runoff = 8+45*np.exp(-((t-8)/3)**2)
    ax.set_axis_off()
    upper = ax.inset_axes([0, .69, 1, .31])
    upper.bar(t, precip, color='#296795', width=.85)
    upper.set(ylim=(30, 0), ylabel='Rain (mm)')
    upper.set_xticks([])
    lower = ax.inset_axes([0, 0, 1, .60])
    lower.plot(t, runoff, color='#529E98', lw=1.8)
    lower.set(ylim=(0, 65), xlabel='Day', ylabel='Discharge (m$^3$ s$^{-1}$)')
    upper.set_xlim(-1, 20)
    lower.set_xlim(-1, 20)
    ax = axes[2, 1]
    flow = np.sort(rng.lognormal(2, .85, 365))[::-1]
    ax.semilogy(np.arange(1, 366)/366*100, flow, color='#296795')
    ax.set(xlabel='Exceedance probability (%)', ylabel='Discharge (m$^3$ s$^{-1}$)')
    ax = axes[2, 2]
    obs = rng.gamma(2, 8, 250)
    sim = np.maximum(0, obs+rng.normal(0, 5, len(obs)))
    ax.scatter(obs, sim, s=11, alpha=.45, color='#296795', edgecolors='none')
    ax.plot([0, 65], [0, 65], color='.4', ls='--', lw=1)
    ax.set(xlim=(0, 65), ylim=(0, 65), xlabel='Observed (example units)', ylabel='Simulated (example units)')
    ax.set_aspect('equal')
    ax = axes[3, 0]
    probability = rng.uniform(0, 1, 1500)
    outcome = rng.binomial(1, probability)
    groups = np.digitize(probability, np.linspace(0, 1, 11))-1
    means = [probability[groups == i].mean() for i in range(10)]
    rates = [outcome[groups == i].mean() for i in range(10)]
    ax.plot([0, 1], [0, 1], color='.5', ls='--', lw=.8)
    ax.plot(means, rates, 'o-', color='#296795', ms=4)
    ax.set(xlabel='Forecast probability', ylabel='Observed frequency', xlim=(0, 1), ylim=(0, 1))
    ax.text(.05, .87, 'Synthetic Bernoulli sample', transform=ax.transAxes, fontsize=7)
    ax = axes[3, 1]
    ax.plot(t, np.sin(t/3), color='#296795')
    ax.axhline(0, color='.6', lw=.8)
    ax.set(xlabel='Time step', ylabel='Coefficient (illustrative units)')
    inset = ax.inset_axes([.52, .60, .43, .33])
    inset.imshow(anomaly, origin='lower', cmap=mpl_cmap('RdBu_r'), vmin=-2, vmax=2, aspect='auto')
    inset.set_xticks([])
    inset.set_yticks([])
    inset.set_title('Synthetic pattern', fontsize=7)
    ax = axes[3, 2]
    ax.remove()
    ax = fig.add_subplot(4, 3, 12, projection='polar')
    angle = np.linspace(0, 2*np.pi, 16, endpoint=False)
    frequency = 5+4*np.cos(angle-.7)**2
    frequency = frequency/frequency.sum()*100
    ax.bar(angle, frequency, width=2*np.pi/16*.85, color='#529E98', alpha=.9)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title('l  Directional frequency', loc='left', fontsize=11, pad=15)
    ax.set_yticks([5, 10], ['5%', '10%'])
    ax.text(.5, -.13, 'Synthetic directions; define from/to in real data', transform=ax.transAxes,
            ha='center', fontsize=7)
    fig.suptitle('COMMON METEOROLOGY + HYDROLOGY PLOTS\nSynthetic teaching examples | Matplotlib backend | Not research results', fontsize=17)
    save(fig, out / 'common_plot_gallery')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    atlas(args.out)
    gallery(args.out)
    print(args.out.resolve())


if __name__ == '__main__':
    main()
