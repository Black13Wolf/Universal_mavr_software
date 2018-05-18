def get_ps(path_to_dat, diff=0, acf=False, save=False, shape=(512,512), output=False, rmbgr_on=True):
    from numpy import memmap, zeros, fft, any
    from os.path import basename, join
    if output:
        output_file = join(output, basename(path_to_dat))
    else:
        output_file = path_to_dat
    serie = memmap(path_to_dat, dtype='uint16').astype('float32')
    if shape == (512, 640): lims = (512, 640)
    else: lims = (512,512)
    frames = int(serie.size/lims[0]/lims[1])
    serie = serie.reshape((frames, lims[0], lims[1]))

    serie, frames = partickle_searcher(serie, path_to_dat, output_file, output)

    output_ps = zeros(shape)
    for num in range(frames):
        frame = zeros(shape)
        if diff and num<frames-diff:
            frame[:lims[0], :lims[1]] += serie[num] - serie[num+diff]
            frame[:lims[0], :lims[1]] += serie[num] - serie[num+diff]
        else:
            frame[:lims[0], :lims[1]] += serie[num]
        output_ps += abs(fft.fft2(frame)**2)                                                                                                                                                                                                                                                                                                                                                                                            
    output_ps /= frames  
    if rmbgr_on: 
        output_ps = fft.fftshift(rmbgr(fft.fftshift(output_ps), 100))
    #output_ps[500:524, 500:524] = 0 Устранение центрального пика СПМ. Сделать сглаживание в будущем.
          
    if acf: output_acf = abs(fft.ifft2(fft.fftshift(output_ps)))
    if save:
        if save == 'fits':
            from astropy.io import fits
            fits.writeto(output_file+'_ps_diff{}_shape{}.{}'.format(diff, shape, save), fft.fftshift(output_ps))
            if acf: fits.writeto(output_file+'_acf_diff{}_shape{}.{}'.format(diff, shape, save), fft.fftshift(output_acf))
        else:
            print('Unknown format: {}'.format(save))
        import gc
        memory = gc.collect()
        print('Очищено объектов из памяти: {}'.format(memory))
    else:
        if acf:
            return fft.fftshift(output_ps), fft.fftshift(output_acf)
        else:
            return fft.fftshift(output_ps)
    
def rmbgr(middle_star, xlim): 
    from numpy import mean
    outbound = middle_star[0:xlim] 
    slice_out = mean(outbound, axis=0) 
    middle_star_clean = middle_star - slice_out 
    return middle_star_clean 

def partickle_searcher(data, name, output_path, log_path):
    print('Поиск частиц')
    print(data.shape)
    from numpy import std, array, mean, where, delete, save
    from matplotlib.pyplot import clf, plot, savefig, hlines
    from os.path import join
    
    sf = data.shape[0]
    mvs = []
    for i in data:
        mvs.append(i.max())
    mvs = array(mvs)
    mvs -= mvs.min()
    mvs /= mvs.max()
    ad = mean(mvs)
    print('Коэфф: {:.2f}'.format(ad))
    plot(mvs)
    k = mean(mvs)*2 + std(mvs)*4
    hlines(k, 0, data.shape[0], color='red')
    savefig(output_path+'.maxvalues.png')
    clf()
    bad_frames = where(mvs > k)[0]
    
    if 0 < len(bad_frames) < data.shape[0] * 0.025:
        data = delete(data, bad_frames, axis = 0)
    print('Конец поиска частиц')
    with open(join(log_path, 'logfile.txt'), 'a+') as log:
        log.write('{}\t koeff: {:.2f}\t Bad frames: {}({:.2f}) \t {}\n'.format(name, ad, len(bad_frames), (len(bad_frames)/sf)*100, str(bad_frames)))
    return data, data.shape[0]
