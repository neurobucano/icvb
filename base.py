import os
import pandas as pd
import numpy as np

class SessionHnd:
  def __init__(self, data_path, default_session_list=True):
    self.data_path = data_path
    self.sessions=pd.read_hdf('%s/ecephys_sessions.h5' % data_path)
    if (default_session_list):
        self.session_ids = [1055415082, 1118512505, 1044594870, 1130349290, 1081431006,1055403683, 1063010385, 1067781390, 1117148442, 1120251466]
    else:
        self._set_session_ids()

  def _set_session_ids(self):
    session_ids=[]
    for filename in os.listdir(self.data_path):
      if filename.startswith('1'):
        session_ids.append(int(filename[0:10]))
    session_ids=list(set(session_ids))
    self.session_ids = session_ids

  def get_acronyms_for_session(self, session_id):
    session_id=int(session_id)
    if session_id not in self.session_ids:
        raise KeyError("A session_id '{}' não foi encontrada.".format(session_id))

    acronyms=self.sessions.loc[session_id].structure_acronyms
    acronyms=acronyms.split("'")[1:-1]
    while (', ' in acronyms):
      acronyms.remove(', ')
    acronyms.remove('root') # Remove root
    acronyms = [item for item in acronyms if not item.startswith('DG-')]
    acronyms.append('DG')
    acronyms.sort()
    L=[]
    for acronym in acronyms:
      if (self.exists_session_for(session_id, acronym)):
        L.append(acronym)
    acronyms = L
    return (acronyms)

  def get_sessions_for (self, acronym):

    sessions = []
    for session_id in self.session_ids:
      if (self.exists_session_for(session_id, acronym)):
        sessions.append(session_id)
    return (sessions)

  def exists_session_for(self, session_id, acronym):
    session_id = int(session_id)
    filename = '%s/%d-%s-spk.h5' % (self.data_path, session_id, acronym)
    #if (session_id==1055415082):
    #print (filename,os.path.exists(filename))
    return (os.path.exists(filename))

  def get_spikes (self, session_id, acronym):
    spikes=None

    filename_spk='%s/%s-%s-spk.h5' % (self.data_path,session_id,acronym)
    if not os.path.exists(filename_spk):
        return (spikes)

    spikes = pd.read_hdf(filename_spk, key='spk')
    spikes.name = '%s-%s' % (session_id,acronym)
    spikes=spikes.sort_index()
    return (spikes)

  def get_speed_run (self, session_id):
    session_id=int(session_id)
    filename = '%s/behavior/%d-comp-vel.h5' % (self.data_path,session_id)
    if not os.path.exists(filename):
        raise FileNotFoundError("File not found '{}'.".format(filename))
    v=pd.read_hdf (filename)
    return (v)

  def get_reward (self, session_id):
    filename = '%s/%d-rew.h5' % (self.data_path,session_id)
    reward = pd.read_hdf(filename)
    return (reward)

  def get_stim (self, session_id):
    filename = '%s/%d-stim.h5' % (self.data_path,session_id)
    stim = pd.read_hdf(filename)
    return (stim)

  def get_stim_times_natural_and_gabor_novel (self, session_id):

    stim = self.get_stim(session_id=session_id)
    stim_natural=stim[stim.stimulus_block==0]
    stim_gabor=stim[stim.stimulus_block==2]
    t_natural = stim_natural.start_time.values
    t_gabor = stim_gabor.start_time.values
    return (t_natural,t_gabor)

  def get_stim_times (self, stim_name, session_id):
    stim = self.get_stim (session_id)
    times = None
    stim_names = {'natural': 'Nat', 'spont': 'spont', 'gabor': 'gabor', 'flash': 'flash'}
    if (stim_name in stim_names.keys()):
      N=stim.stimulus_name.str.startswith(stim_names[stim_name])
      times=stim[N]['start_time'].dropna().values
    return (times)

  def get_stim_block_period(self, session_id, block_id):
    '''Dado identificador de uma sessão, retornar uma tupla com início e o final
    daquele block '''

    stim = self.get_stim(session_id)
    a=stim[stim.stimulus_block==block_id]['start_time'].values[0]
    b=stim[stim.stimulus_block==block_id]['end_time'].values[-1]
    return (a,b)

  def get_file_map(self, session_id):

    areas = self.get_acronyms_for_session(session_id)
    file_map=pd.DataFrame()
    for area in areas:
      filename='%s/%d-%s-spk.h5' % (data_path,session_id,area)
      spikes=pd.read_hdf(filename)
      units = spikes.unique()
      tmp=pd.DataFrame(index=units)
      tmp['session_id']=session_id
      tmp['area']=area
      file_map=pd.concat([file_map,tmp])
    return (file_map)

  def build_file_maps(self):    
        n_procs = int(max(cpu_count(),1))
        with Pool(n_procs) as p:
            result=p.map(unit_file_map, session_ids)
        self.file_map =pd.concat(result)
      
  def build_file_maps(self):
        from multiprocessing import Pool, cpu_count
        n_procs = int(max(cpu_count(), 1))
        with Pool(n_procs) as p:
            result = p.map(unit_file_map, session_ids)
        self.file_map = pd.concat(result)
