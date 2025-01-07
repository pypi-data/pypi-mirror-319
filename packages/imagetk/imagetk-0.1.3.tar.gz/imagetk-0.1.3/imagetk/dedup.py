# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:12:52 2024

@author: ThinkPad
"""
import os
import numpy
from typing import Callable, Dict, Union, Tuple, List, Literal
from multiprocessing import cpu_count
from scient.image import hash
# from .process import convert_gray,resize
from scient.algorithm import bktree,distance
from scient import process
from io import BytesIO
from PIL import Image

class Hash:
    def __init__(self,hash_func:Callable=hash.percept,dist_func:Callable=distance.hamming,process_func:Callable=None,
                 threshold:int=10,hash_size:int=64,hash_hex:bool=False,
                 errors:Literal['ignore','raise','coerce']='raise',
                 suffix:Union[str,List[str]]=['JPEG', 'PNG', 'BMP', 'MPO', 'PPM', 'TIFF', 'GIF', 'WEBP', 'JPG'],
                 progress:bool=True,n_worker:int=cpu_count()):
        '''
        
        Parameters
        ----------
        hash_func : Callable, optional
            hash函数. The default is hash.percept.
        dist_func : Callable, optional
            距离度量函数. The default is distance.hamming.
        process_func : Callable, optional
            图像预处理函数，如果为空，采用self.process. The default is None.
        threshold : int, optional
            图像重复的判断阈值，根据dist_func计算距离，若距离小于threshold，判断为重复图像. The default is 10.
        hash_size : int, optional
            hash值长度. The default is 64.
        hash_hex : bool, optional
            hash_func是否转成16进制，转成16进制可以节省存储空间. The default is False.
        errors : str, optional
            图像加载/查重错误时的处理方式，可选值为['ignore','raise','coerce'],'ignore'忽略文件,'raise'抛出异常,'coerce'强制转成空图像,. The default is 'ignore'.
        suffix : str or list, optional
            可以处理的图像文件后缀名. The default is ['JPEG', 'PNG', 'BMP', 'MPO', 'PPM', 'TIFF', 'GIF', 'WEBP'].
        n_worker : int, optional
            并行处理进程数. The default is cpu_count().

        Returns
        -------
        None.

        '''
        self.hash_func=hash_func
        self.dist_func=dist_func
        if process_func is not None:
            self.process=process_func
            
        self.threshold=threshold
        self.hash_size=hash_size
        self.hash_hex=hash_hex
        self.progress=progress
        self.n_worker=n_worker
        
        self.errors=errors
        self.suffix=suffix

    def encode(self,image:numpy.ndarray):#编码图片
        return self.hash_func(image,hash_size=self.hash_size,hash_hex=self.hash_hex)

    def encode_file(self,file:Union[str,BytesIO]):#编码图片文件
        #load
        image=self.load(file)
        if image is None:
            return
        #process
        if self.process is not None:
            image=self.process(image)
        return self.encode(image)
    
    def encode_files(self,files:List,return_dict:bool=True):#编码一批图片文件
        # print('encoding files...')
        encodes=process.pool(self.encode_file,files,self.n_worker,desc='encode files',progress=self.progress)
        if return_dict:#zip压缩包内的文件没有文件名，不返回dict
            encodes=dict(zip(files,encodes))
            encodes={k:v for k,v in encodes.items() if v is not None}#处理errors='ignore'的load失败
        return encodes

    def encode_folder(self,path):#编码文件夹内图片文件
        assert os.path.isdir(path)
        
        files=process.ls_R(path)
        #filt_suffix
        if self.suffix is not None:
            files=self.filt_suffix(files)
        #encode
        encode_map=self.encode_files(files)
        #relative path
        encode_map={os.path.relpath(k,path):v for k,v in encode_map.items()}
        return encode_map
    '''
    def encode_zipfile(self,path):#编码zip压缩包内图片文件
        assert zipfile.is_zipfile(path)
        
        zf=zipfile.ZipFile(path)
        files=zf.namelist()
        #filt_suffix
        if self.suffix is not None:
            files=self.filt_suffix(files)
        print('zipfile bytesio...')
        bytesio=[BytesIO(zf.read(i)) for i in tqdm(files)]
        #encode
        encodes=self.encode_files(bytesio,return_dict=False)
        encode_map=dict(zip(files,encodes))
        encode_map={k:v for k,v in encode_map.items() if v is not None}#处理errors='ignore'的load失败
        return encode_map
    '''
    def encode_archive(self,path,mode='zipfile'):#编码zip压缩包内图片文件
        from tqdm import tqdm
        if mode=='zipfile':
            import zipfile
            archive=zipfile.ZipFile(path)
            file_names=[i.filename for i in archive.filelist if not i.is_dir()]
            #filt_suffix
            if self.suffix is not None:
                file_names=self.filt_suffix(file_names)
            # print('archive file bytesio...')
            # files=[archive.open(i) for i in file_names]#会报错：cannot pickle 'BufferedReader' instances
            files=[BytesIO(archive.read(i)) for i in tqdm(file_names,desc='archive to bytesio',disable=not self.progress)]
        elif mode=='tarfile':
            import tarfile
            archive=tarfile.open(path)
            file_names=[i.name for i in archive.getmembers() if i.isfile()]
            #filt_suffix
            if self.suffix is not None:
                file_names=self.filt_suffix(file_names)
            # print('archive file bytesio...')
            files=[BytesIO(archive.extractfile(i).read()) for i in tqdm(file_names,desc='archive to bytesio',disable=not self.progress)]
        else:
            raise ValueError('mode must be zipfile or tarfile.')
        #encode
        encodes=self.encode_files(files,return_dict=False)
        encode_map=dict(zip(file_names,encodes))
        encode_map={k:v for k,v in encode_map.items() if v is not None}#处理errors='ignore'的load失败
        return encode_map
        
    def find_dup_from_map(self,encode,encode_map:Dict=None):
        #从字典/pandas.Series等映射对象中找与当前图像重复的图像
        if encode_map is None:#并行任务时，只能传一个参数，用encode接收后拆解
            encode,encode_map=encode
        if self.hash_hex:#处理hash_hex
            encode = bin(int(encode, 16))[2:].zfill(self.hash_size)
            encode_map={k:bin(int(v, 16))[2:].zfill(self.hash_size) for k,v in encode_map.items()}
        tree = bktree.BKTree(encode_map, self.dist_func)  # construct bktree
        result=tree.search(query=encode,tol=self.threshold)  #search
        result=sorted(result,key=lambda x:x[1])  #sorted
        return result

    def find_dup_in_map(self,encode_map:Dict,score:Dict=None):
        #在字典/pandas.Series等映射对象中找重复的图像
        # print('finding duplicates...')
        if score is None:
            args=[(v,encode_map) for k,v in encode_map.items()]
            result=process.pool(self.find_dup_from_map,args,self.n_worker,desc='find duplicates',progress=self.progress)
            result=dict(zip([k for k,v in encode_map.items()],result))
        else:
            from tqdm import tqdm
            score_sort=sorted(list(score.items()),key=lambda x:x[1],reverse=True)
            result={}
            for k,v in tqdm(score_sort,desc='find duplicates',disable=not self.progress):
                if self.errors=='ignore' and k not in encode_map:#处理errors='ignore'的查重失败
                    continue
                if k in result:
                    continue
                if k in [i[0] for i in sum(result.values(),[])]:
                    continue
                result[k]=self.find_dup_from_map(encode_map[k],encode_map)
        
        result={k:[i for i in v if i[0]!=k] for k,v in result.items()}#去掉与比对文件同名的文件
        return result
    
    def find_dup_from_files(self,file,files):
        #从一批文件中找与当前图像重复的图像
        #encode
        encode=self.encode_file(file)
        assert encode is not None #处理errors='ignore'的load失败
        encode_map=self.encode_files(files)
        return self.find_dup_from_map(encode,encode_map)

    def find_dup_in_files(self,files,score:Dict=None):
        #在一批文件中找重复的图像
        #encode
        encode_map=self.encode_files(files)
        return self.find_dup_in_map(encode_map,score)

    def find_dup_from_folder(self,file,path:str):
        #从文件夹中找与当前图像重复的图像
        assert os.path.isfile(file)
        assert os.path.isdir(path)
        
        files=process.ls_R(path)
        #filt_suffix
        if self.suffix is not None:
            files=self.filt_suffix(files)
        
        #encode
        encode=self.encode_file(file)
        assert encode is not None #处理errors='ignore'的load失败
        encode_map=self.encode_files(files)
        #relative path
        encode_map={os.path.relpath(k,path):v for k,v in encode_map.items()}

        return self.find_dup_from_map(encode,encode_map)

    def find_dup_in_folder(self,path:str,score:Dict=None):
        #在文件夹中找重复的图像
        assert os.path.isdir(path)
        
        files=process.ls_R(path)
        if self.suffix is not None:
            files=self.filt_suffix(files)
        
        #encode
        encode_map=self.encode_files(files)
        #relative path
        encode_map={os.path.relpath(k,path):v for k,v in encode_map.items()}
        return self.find_dup_in_map(encode_map,score)
    '''
    def find_dup_from_zipfile(self,file,path):
        #从zip包中找与当前图像重复的图像
        assert os.path.isfile(file)
        assert zipfile.is_zipfile(path)
        #encode
        encode=self.encode_file(file)
        assert encode is not None #处理errors='ignore'的load失败
        encode_map=self.encode_zipfile(path)
        return self.find_dup_from_map(encode,encode_map)
        
    def find_dup_in_zipfile(self,path,score=None):
        #在zip包中找重复的图像
        assert zipfile.is_zipfile(path)
        
        #encode
        encode_map=self.encode_zipfile(path)
        return self.find_dup_in_map(encode_map,score)
    '''
    def find_dup_from_archive(self,file,path,mode='zipfile'):
        #从zip/tar打包文件中找与当前图像重复的图像
        assert os.path.isfile(file)
        #encode
        encode=self.encode_file(file)
        assert encode is not None #处理errors='ignore'的load失败
        encode_map=self.encode_archive(path,mode=mode)
        return self.find_dup_from_map(encode,encode_map)
    
    def find_dup_in_archive(self,path,score=None,mode='zipfile'):
        #在zip/tar打包文件中找重复的图像
        #encode
        encode_map=self.encode_archive(path,mode=mode)
        return self.find_dup_in_map(encode_map,score)

    def load(self,file:Union[str,BytesIO])->numpy.ndarray:
        #加载图片
        try:
            image=Image.open(file)
        except:
            if self.errors=='ignore':
                image=None
                print(file,'load failed, load return None')
            elif self.errors=='raise':
                raise ValueError(file,'load failed!')
            elif self.errors=='coerce':
                image=Image.new('RGB', size=(1, 1))
                print(file,'load failed, coerce to empty image')
            else:
                raise ValueError('errors must be in ["ignore","raise","coerce"]!')
                
        # return numpy.array(image)
        image=image.convert('L')
        return numpy.array(image)
    '''
    def process(self,image:numpy.ndarray) -> numpy.ndarray:
        #处理图片
        #scale
        if self.scale is not None:
            image = resize(image,size=self.scale)
        #gray
        image = convert_gray(image)
        
        #输出numpy.array
        return image.astype('uint8')
    '''
    def filt_suffix(self,files:List[str])->List:
        #根据文件后缀名过滤图片文件
        if isinstance(self.suffix,str):
            files=[i for i in files if i.lower().endswith(self.suffix.lower())]
        elif isinstance(self.suffix,(list,tuple)):
            files=[i for i in files if any([i.lower().endswith(j.lower()) for j in self.suffix])]
        elif self.suffix is not None:
            raise ValueError('suffix must not be None!')
        return files
    
