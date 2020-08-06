from neuron import h

class modelcell():
    def __init__(self):
        self.x = 0; self.y = 0; self.z = 0

        self.gid = -1
        self.core_i=-1
        self.coretype_i=-1
        
        self.is_art = 0
        self.nc = []
        self.pre_list = []

class GranuleCell(modelcell):
    """ Granule Cell definition """
    def __init__(self, gid = -1):
        super().__init__()
        self.gid = gid
        self.create_sections() 
        self.build_topology()
        self.build_subsets() # subsets()
        self.define_geometry() # geom()
        self.define_biophysics() # biophys()
        self.addSynapses() # synapses
        
    def __repr__(self):
        return "Pyramidal Cell {}".format(self.gid)

    def create_sections(self):
        self.soma = h.Section(name='soma', cell=self)
		self.gcdend1 = []
		self.gcdend2 = []
		
		for r in range(4):
			self.gcdend1.append(h.Section(name='gcdend1['+str(r)+']', cell=self))
			self.gcdend2.append(h.Section(name='gcdend1['+str(r)+']', cell=self))

    def build_topology(self):
        self.gcdend1[0].connect(self.soma(1))
        self.gcdend2[0].connect(self.soma(1))
		
		for r in range(1,4):
			self.gcdend1[r].connect(self.gcdend1[r-1](1))
			self.gcdend2[r].connect(self.gcdend2[r-1](1))
      

    def define_geometry(self):


	soma {nseg=1 L=16.8 diam=16.8} // changed L & diam
		
	gcdend1 [0] {nseg=1 L=50 diam=3}
	for i = 1, 3	gcdend1 [i] {nseg=1 L=150 diam=3}

	gcdend2 [0] {nseg=1 L=50 diam=3}
	for i = 1, 3	gcdend2 [i] {nseg=1 L=150 diam=3}	 	


        
        self.soma.nseg = 1
        self.soma.L = 16.8
        self.soma.diam = 16.8
		
		self.gcdend1[0].nseg = 1
		self.gcdend1[0].L = 50
		self.gcdend1[0].diam = 3
		
		self.gcdend2[0].nseg = 1
		self.gcdend2[0].L = 50
		self.gcdend2[0].diam = 3

		for r in range(1,4):
			self.gcdend1[r].nseg = 1
			self.gcdend1[r].L = 150
			self.gcdend1[r].diam = 3
			
			self.gcdend2[r].nseg = 1
			self.gcdend2[r].L = 150
			self.gcdend2[r].diam = 3


    def build_subsets(self):
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

		self.gcldend  = h.SectionList()
		self.gcldend.append(self.gcdend1[0])
		self.gcldend.append(self.gcdend2[0])

		self.pdend  = h.SectionList()
		self.pdend.append(self.gcdend1[1])
		self.pdend.append(self.gcdend2[1])

		self.mdend  = h.SectionList()
		self.mdend.append(self.gcdend1[2])
		self.mdend.append(self.gcdend2[2])

		self.ddend  = h.SectionList()
		self.ddend.append(self.gcdend1[3])
		self.ddend.append(self.gcdend2[3])

    def define_biophysics(self):


        for sec in self.all:
            sec.insert("ccanl")
			sec.catau_ccanl = 10
			sec.caiinf_ccanl = 5.e-6
            sec.Ra = 210
			
        
        self.soma.insert("ichan2") # modified from Aradi and Soltesz 2002
        self.soma.insert("borgka") # KA from Aradi and Soltesz 2002
        self.soma.insert("nca") # NVA Ca++-L type current
        self.soma.insert("lca") # HVA Ca++-L type current
        self.soma.insert("cat") # m-type potassium current
        self.soma.insert("gskch") # SK channel from Aradi and Soltesz 2002
        self.soma.insert("cagk") # from Migliore et al., 1995

        for seg in self.soma:
            seg.cm = 1 			
            seg.gnatbar_ichan2=0.12  
            seg.gkfbar_ichan2=0.016  
            seg.gksbar_ichan2=0.006
            seg.gl_ichan2=0.006		
			seg.gkabar_borgka=0.012			
			seg.gncabar_nca=0.002			
			seg.glcabar_lca=0.005		
			seg.gcatbar_cat=0.000037
			seg.gskbar_gskch=0.001
			seg.gkbar_cagk=0.0006

        for sec in self.gcldend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002
			sec.insert("nca") # NVA Ca++-L type current
			sec.insert("lca") # HVA Ca++-L type current
			sec.insert("cat") # m-type potassium current
			sec.insert("gskch") # SK channel from Aradi and Soltesz 2002
			sec.insert("cagk") # from Migliore et al., 1995

			for seg in sec:
				seg.cm = 1 			
				seg.gnatbar_ichan2=0.018  
				seg.gkfbar_ichan2=0.004  
				seg.gksbar_ichan2=0.006
				seg.gl_ichan2=0.00004		
				seg.gncabar_nca=0.003			
				seg.glcabar_lca=0.0075		
				seg.gcatbar_cat=0.000075
				seg.gskbar_gskch=0.0004
				seg.gkbar_cagk=0.0006


        for sec in self.pdend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002
			sec.insert("nca") # NVA Ca++-L type current
			sec.insert("lca") # HVA Ca++-L type current
			sec.insert("cat") # m-type potassium current
			sec.insert("gskch") # SK channel from Aradi and Soltesz 2002
			sec.insert("cagk") # from Migliore et al., 1995

			for seg in sec:
				seg.cm = 1.6		
				seg.gnatbar_ichan2=0.013  
				seg.gkfbar_ichan2=0.004  
				seg.gksbar_ichan2=0.006
				seg.gl_ichan2=0.000063		
				seg.gncabar_nca=0.001			
				seg.glcabar_lca=0.0075		
				seg.gcatbar_cat=0.00025
				seg.gskbar_gskch=0.0002
				seg.gkbar_cagk=0.001

        for sec in self.mdend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002
			sec.insert("nca") # NVA Ca++-L type current
			sec.insert("lca") # HVA Ca++-L type current
			sec.insert("cat") # m-type potassium current
			sec.insert("gskch") # SK channel from Aradi and Soltesz 2002
			sec.insert("cagk") # from Migliore et al., 1995

			for seg in sec:
				seg.cm = 1.6		
				seg.gnatbar_ichan2=0.008  
				seg.gkfbar_ichan2=0.001  
				seg.gksbar_ichan2=0.006
				seg.gl_ichan2=0.000063		
				seg.gncabar_nca=0.001			
				seg.glcabar_lca=0.0005		
				seg.gcatbar_cat=0.0005
				seg.gskbar_gskch=0.0
				seg.gkbar_cagk=0.0024


        for sec in self.ddend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002
			sec.insert("nca") # NVA Ca++-L type current
			sec.insert("lca") # HVA Ca++-L type current
			sec.insert("cat") # m-type potassium current
			sec.insert("gskch") # SK channel from Aradi and Soltesz 2002
			sec.insert("cagk") # from Migliore et al., 1995

			for seg in sec:
				seg.cm = 1.6		
				seg.gnatbar_ichan2=0.0  
				seg.gkfbar_ichan2=0.001  
				seg.gksbar_ichan2=0.008
				seg.gl_ichan2=0.000063		
				seg.gncabar_nca=0.001			
				seg.glcabar_lca=0.00		
				seg.gcatbar_cat=0.001
				seg.gskbar_gskch=0.0
				seg.gkbar_cagk=0.0024


        for sec in self.all:
			sec.enat = 45
			sec.ekf = -90
			sec.eks = -90
			sec.ek=-90
			sec.elca=130
			sec.etca=130
			sec.esk=-90
			sec.el_ichan2 =-70
			sec.cao_ccanl=2             


    def connect2target(self,target, delay = 1, weight=0.04): # { localobj nc #$o1 target point process, optional $o2 returned NetCon
        self.nc.append(h.NetCon(self.soma(0.5)._ref_v, target, sec=self.soma))
        self.nc[-1].threshold = -10 # mV
        self.nc[-1].delay = delay # ms
        self.nc[-1].weight[0] = weight # NetCon weight is a vector    
        return self.nc[-1]


    def addSynapses(self):
        self.pre_list = []

        # PP syn based on data from Greg Hollrigel and Kevin Staley
        syn_ = h.Exp2Syn(self.gcdend1[3](0.5))
        self.pre_list.append(syn_)  
        syn_.tau1 = 1.5
        syn_.tau2 = 5.5
        syn_.e = 0
        
        # PPsyn based on Greg and Staley
        syn_ = h.Exp2Syn(self.gcdend2[3](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 1.5
        syn_.tau2 = 5.5
        syn_.e = 0
        
        # MC syn *** Estimated
        syn_ = h.Exp2Syn(self.gcdend1[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 1.5
        syn_.tau2 = 5.5
        syn_.e = 0
        
        # MC syn *** Estimated
        syn_ = h.Exp2Syn(self.gcdend2[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 1.5
        syn_.tau2 = 5.5
        syn_.e = 0
        
        # HIPP  syn based on Harney and Jones corrected for temp
        syn_ = h.Exp2Syn(self.gcdend1[3](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.5
        syn_.tau2 = 6
        syn_.e = -70
        
        # HIPP  syn based on Harney and Jones corrected for temp
        syn_ = h.Exp2Syn(self.gcdend2[3](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.5
        syn_.tau2 = 6
        syn_.e = -70
        
        #  BC  syn syn based on Bartos
        syn_ = h.Exp2Syn(self.soma(0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.26
        syn_.tau2 = 5.5
        syn_.e = -70
        
        #  NOTE: SPROUTED SYNAPSE based on Molnar and Nadler
        syn_ = h.Exp2Syn(self.gcdend1[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 1.5
        syn_.tau2 = 5.5
        syn_.e = 0
        
        #  NOTE: SPROUTED SYNAPSE based on Molnar and Nadler
        syn_ = h.Exp2Syn(self.gcdend2[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 1.5
        syn_.tau2 = 5.5
        syn_.e = 0
		# Total of 7 synapses per GC 0,1 PP; 	2,3 MC;	4,5 HIPP and 	6 BC	7,8 Sprout

class BasketCell(modelcell):
    """ Basket Cell definition """
    def __init__(self, gid = -1):
        super().__init__()
        self.gid = gid
        self.create_sections() 
        self.build_topology()
        self.build_subsets() # subsets()
        self.define_geometry() # geom()
        self.define_biophysics() # biophys()
        self.addSynapses() # synapses
        
    def __repr__(self):
        return "Basket Cell {}".format(self.gid)

    def create_sections(self):
        self.soma = h.Section(name='soma', cell=self)
		self.bcdend1 = []
		self.bcdend2 = []
		self.bcdend3 = []
		self.bcdend4 = []
		
		for r in range(4):
			self.bcdend1.append(h.Section(name='bcdend1['+str(r)+']', cell=self))
			self.bcdend2.append(h.Section(name='bcdend2['+str(r)+']', cell=self))
			self.bcdend3.append(h.Section(name='bcdend3['+str(r)+']', cell=self))
			self.bcdend4.append(h.Section(name='bcdend4['+str(r)+']', cell=self))

    def build_topology(self):
        self.bcdend1[0].connect(self.soma(1))
        self.bcdend2[0].connect(self.soma(1))
        self.bcdend3[0].connect(self.soma(0))
        self.bcdend4[0].connect(self.soma(0))
		
		for r in range(1,4):
			self.bcdend1[r].connect(self.bcdend1[r-1](1))
			self.bcdend2[r].connect(self.bcdend2[r-1](1))
			self.bcdend3[r].connect(self.bcdend3[r-1](1))
			self.bcdend4[r].connect(self.bcdend4[r-1](1))
      

    def define_geometry(self):
		self.soma.nseg=1 
		self.soma.L=20 
		self.soma.diam=15

		for r in range(4):
			self.bcdend1[r].nseg=1 
			self.bcdend1[r].L=75 
			self.bcdend1[r].diam=4-r

			self.bcdend2[r].nseg=1 
			self.bcdend2[r].L=75 
			self.bcdend2[r].diam=4-r

			self.bcdend3[r].nseg=1 
			self.bcdend3[r].L=75 
			self.bcdend3[r].diam=4-r

			self.bcdend4[r].nseg=1 
			self.bcdend4[r].L=75 
			self.bcdend4[r].diam=4-r

    def build_subsets(self):
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

		self.adend  = h.SectionList()
		self.adend.append(self.bcdend1[0])
		self.adend.append(self.bcdend2[0])
		self.adend.append(self.bcdend3[0])
		self.adend.append(self.bcdend4[0])

		self.bdend  = h.SectionList()
		self.bdend.append(self.bcdend1[1])
		self.bdend.append(self.bcdend2[1])
		self.bdend.append(self.bcdend3[1])
		self.bdend.append(self.bcdend4[1])

		self.cdend  = h.SectionList()
		self.cdend.append(self.bcdend1[2])
		self.cdend.append(self.bcdend2[2])
		self.cdend.append(self.bcdend3[2])
		self.cdend.append(self.bcdend4[2])

		self.ddend  = h.SectionList()
		self.ddend.append(self.bcdend1[3])
		self.ddend.append(self.bcdend2[3])
		self.ddend.append(self.bcdend3[3])
		self.ddend.append(self.bcdend4[3])

    def define_biophysics(self):      
        self.soma.insert("ichan2") # modified from Aradi and Soltesz 2002
        self.soma.insert("borgka") # KA from Aradi and Soltesz 2002
        self.soma.insert("nca") # NVA Ca++-L type current
        self.soma.insert("lca") # HVA Ca++-L type current
        self.soma.insert("cat") # m-type potassium current
        self.soma.insert("gskch") # SK channel from Aradi and Soltesz 2002
        self.soma.insert("cagk") # from Migliore et al., 1995

        for seg in self.soma:
            seg.cm = 1 			
            seg.gnatbar_ichan2=0.12  
            seg.gkfbar_ichan2=0.016  
            seg.gksbar_ichan2=0.006
            seg.gl_ichan2=0.006		
			seg.gkabar_borgka=0.012			
			seg.gncabar_nca=0.002			
			seg.glcabar_lca=0.005		
			seg.gcatbar_cat=0.000037
			seg.gskbar_gskch=0.001
			seg.gkbar_cagk=0.0006

        for sec in self.gcldend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002
			sec.insert("nca") # NVA Ca++-L type current
			sec.insert("lca") # HVA Ca++-L type current
			sec.insert("cat") # m-type potassium current
			sec.insert("gskch") # SK channel from Aradi and Soltesz 2002
			sec.insert("cagk") # from Migliore et al., 1995

			for seg in sec:
				seg.cm = 1 			
				seg.gnatbar_ichan2=0.018  
				seg.gkfbar_ichan2=0.004  
				seg.gksbar_ichan2=0.006
				seg.gl_ichan2=0.00004		
				seg.gncabar_nca=0.003			
				seg.glcabar_lca=0.0075		
				seg.gcatbar_cat=0.000075
				seg.gskbar_gskch=0.0004
				seg.gkbar_cagk=0.0006


        for sec in self.pdend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002
			sec.insert("nca") # NVA Ca++-L type current
			sec.insert("lca") # HVA Ca++-L type current
			sec.insert("cat") # m-type potassium current
			sec.insert("gskch") # SK channel from Aradi and Soltesz 2002
			sec.insert("cagk") # from Migliore et al., 1995

			for seg in sec:
				seg.cm = 1.6		
				seg.gnatbar_ichan2=0.013  
				seg.gkfbar_ichan2=0.004  
				seg.gksbar_ichan2=0.006
				seg.gl_ichan2=0.000063		
				seg.gncabar_nca=0.001			
				seg.glcabar_lca=0.0075		
				seg.gcatbar_cat=0.00025
				seg.gskbar_gskch=0.0002
				seg.gkbar_cagk=0.001

        for sec in self.mdend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002
			sec.insert("nca") # NVA Ca++-L type current
			sec.insert("lca") # HVA Ca++-L type current
			sec.insert("cat") # m-type potassium current
			sec.insert("gskch") # SK channel from Aradi and Soltesz 2002
			sec.insert("cagk") # from Migliore et al., 1995

			for seg in sec:
				seg.cm = 1.6		
				seg.gnatbar_ichan2=0.008  
				seg.gkfbar_ichan2=0.001  
				seg.gksbar_ichan2=0.006
				seg.gl_ichan2=0.000063		
				seg.gncabar_nca=0.001			
				seg.glcabar_lca=0.0005		
				seg.gcatbar_cat=0.0005
				seg.gskbar_gskch=0.0
				seg.gkbar_cagk=0.0024


        for sec in self.ddend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002
			sec.insert("nca") # NVA Ca++-L type current
			sec.insert("lca") # HVA Ca++-L type current
			sec.insert("cat") # m-type potassium current
			sec.insert("gskch") # SK channel from Aradi and Soltesz 2002
			sec.insert("cagk") # from Migliore et al., 1995

			for seg in sec:
				seg.cm = 1.6		
				seg.gnatbar_ichan2=0.0  
				seg.gkfbar_ichan2=0.001  
				seg.gksbar_ichan2=0.008
				seg.gl_ichan2=0.000063		
				seg.gncabar_nca=0.001			
				seg.glcabar_lca=0.00		
				seg.gcatbar_cat=0.001
				seg.gskbar_gskch=0.0
				seg.gkbar_cagk=0.0024


        for sec in self.all:
			sec.enat = 55
			sec.ekf = -90
			sec.ek = -90
			sec.esk=-90
			sec.elca=130
			sec.el_ichan2 =-60.06
            sec.Ra = 100


            sec.insert("ccanl")
			sec.catau_ccanl = 10
			sec.caiinf_ccanl = 5.e-6
			sec.cao_ccanl=2             


    def connect2target(self,target, delay = 1, weight=0.04): # { localobj nc #$o1 target point process, optional $o2 returned NetCon
        self.nc.append(h.NetCon(self.soma(0.5)._ref_v, target, sec=self.soma))
        self.nc[-1].threshold = -10 # mV
        self.nc[-1].delay = delay # ms
        self.nc[-1].weight[0] = weight # NetCon weight is a vector    
        return self.nc[-1]


    def addSynapses(self):
        self.pre_list = []

        # PP(AMPA) syn to apical dist dend Dingledine '95
        syn_ = h.Exp2Syn(self.bcdend1[3](0.5))
        self.pre_list.append(syn_)  
        syn_.tau1 = 2
        syn_.tau2 = 6.3
        syn_.e = 0
        
        # PP(AMPA) syn to apical dist dend Dingledine '95
        syn_ = h.Exp2Syn(self.bcdend2[3](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 2
        syn_.tau2 = 6.3
        syn_.e = 0
        
        # GC(AMPA) syn to prox dend Geiger '97
        syn_ = h.Exp2Syn(self.bcdend1[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .3
        syn_.tau2 = .6
        syn_.e = 0
        
        # GC(AMPA) syn to prox dend Geiger '97
        syn_ = h.Exp2Syn(self.bcdend2[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .3
        syn_.tau2 = .6
        syn_.e = 0
        
        # GC(AMPA) syn to prox dend Geiger '97
        syn_ = h.Exp2Syn(self.bcdend3[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .3
        syn_.tau2 = .6
        syn_.e = 0
        
        # GC(AMPA) syn to prox dend Geiger '97
        syn_ = h.Exp2Syn(self.bcdend4[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .3
        syn_.tau2 = .6
        syn_.e = 0
        
        #  MC(AMPA) syn to apical IML dend
        syn_ = h.Exp2Syn(self.bcdend1[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.9
        syn_.tau2 = 3.6
        syn_.e = 0
        
        #  MC(AMPA) syn to apical IML dend
        syn_ = h.Exp2Syn(self.bcdend2[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.9
        syn_.tau2 = 3.6
        syn_.e = 0
        
        #  NOTE: BC(GABA) syn to apical IML dend Bartos
        syn_ = h.Exp2Syn(self.bcdend1[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.16
        syn_.tau2 = 1.8
        syn_.e = -70  
     
        #  NOTE: BC(GABA) syn to apical IML dend Bartos
        syn_ = h.Exp2Syn(self.bcdend2[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.16
        syn_.tau2 = 1.8
        syn_.e = -70  
		        
        #  NOTE: HIPP(GABA) syn to apical distal dend 
        syn_ = h.Exp2Syn(self.bcdend1[3](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.4
        syn_.tau2 = 5.8
        syn_.e = -70
		        
        #  NOTE: HIPP(GABA) syn to apical distal dend 
        syn_ = h.Exp2Syn(self.bcdend2[3](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.4
        syn_.tau2 = 5.8
        syn_.e = -70
		
		# Total of 12 synapses 	0,1 PP; 	2-5 GC; 	6,7 MC; 	8,9 BC; 	10,11 HIPP 

class MossyCell(modelcell):
    """ Mossy Cell definition """
    def __init__(self, gid = -1):
        super().__init__()
        self.gid = gid
        self.create_sections() 
        self.build_topology()
        self.build_subsets() # subsets()
        self.define_geometry() # geom()
        self.define_biophysics() # biophys()
        self.addSynapses() # synapses
        
    def __repr__(self):
        return "Mossy Cell {}".format(self.gid)

    def create_sections(self):
        self.soma = h.Section(name='soma', cell=self)
		self.mcdend1 = []
		self.mcdend2 = []
		self.mcdend3 = []
		self.mcdend4 = []
		
		for r in range(4):
			self.mcdend1.append(h.Section(name='mcdend1['+str(r)+']', cell=self))
			self.mcdend2.append(h.Section(name='mcdend2['+str(r)+']', cell=self))
			self.mcdend3.append(h.Section(name='mcdend3['+str(r)+']', cell=self))
			self.mcdend4.append(h.Section(name='mcdend4['+str(r)+']', cell=self))

    def build_topology(self):
        self.mcdend1[0].connect(self.soma(1))
        self.mcdend2[0].connect(self.soma(1))
        self.mcdend3[0].connect(self.soma(0))
        self.mcdend4[0].connect(self.soma(0))
		
		for r in range(1,4):
			self.mcdend1[r].connect(self.mcdend1[r-1](1))
			self.mcdend2[r].connect(self.mcdend2[r-1](1))
			self.mcdend3[r].connect(self.mcdend3[r-1](1))
			self.mcdend4[r].connect(self.mcdend4[r-1](1))
      

    def define_geometry(self):
		self.soma.nseg=1 
		self.soma.L=20 
		self.soma.diam=20
		
		diamlist=[5.78, 4, 2.5, 1]

		for r in range(4):
			self.mcdend1[r].nseg=1 
			self.mcdend1[r].L=50 
			self.mcdend1[r].diam=diamlist[r]

			self.mcdend2[r].nseg=1 
			self.mcdend2[r].L=50 
			self.mcdend2[r].diam=diamlist[r]

			self.mcdend3[r].nseg=1 
			self.mcdend3[r].L=50 
			self.mcdend3[r].diam=diamlist[r]

			self.mcdend4[r].nseg=1 
			self.mcdend4[r].L=50 
			self.mcdend4[r].diam=diamlist[r]

    def build_subsets(self):
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

		self.pdend  = h.SectionList()
		self.pdend.append(self.mcdend1[0])
		self.pdend.append(self.mcdend2[0])
		self.pdend.append(self.mcdend3[0])
		self.pdend.append(self.mcdend4[0])

		self.ddend  = h.SectionList()
		for r in range(1,4):
			self.ddend.append(self.mcdend1[r])
			self.ddend.append(self.mcdend2[r])
			self.ddend.append(self.mcdend3[r])
			self.ddend.append(self.mcdend4[r])

    def define_biophysics(self):      
        self.soma.insert("ichan2") # modified from Aradi and Soltesz 2002
		self.soma.cm=0.6
		
        for seg in self.soma:
            seg.cm = 1 			
            seg.gnatbar_ichan2=0.12  
            seg.gkfbar_ichan2=0.0005  
            seg.gl_ichan2=0.000011

        for sec in self.pdend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002
			for seg in sec:
				seg.cm = 1 			
				seg.gnatbar_ichan2=0.12  
				seg.gkfbar_ichan2=0.0005  
				seg.gl_ichan2=0.000044		
			sec.cm = 2.4

        for sec in self.ddend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002

			for seg in sec:
				seg.cm = 1.6		
				seg.gnatbar_ichan2=0.0  
				seg.gkfbar_ichan2=0.00 
				seg.gl_ichan2=0.000044		
			sec.cm = 2.4

        for sec in self.all:
        	sec.insert("borgka") # KA from Aradi and Soltesz 2002
        	sec.insert("nca") # NVA Ca++-L type current
        	sec.insert("lca") # HVA Ca++-L type current
        	sec.insert("gskch") # SK channel from Aradi and Soltesz 2002
        	sec.insert("cagk") # from Migliore et al., 1995
        	sec.insert("hyperde3") # from Migliore et al., 1995
            sec.insert("ccanl")
			for seg in sec:
				seg.gkabar_borgka=0.00001			
				seg.gncabar_nca=0.00008			
				seg.glcabar_lca=0.0006		
				seg.gskbar_gskch=0.016
				seg.gkbar_cagk=0.0165
				seg.ghyfbar_hyperde3=0.000005
				seg.ghysbar_hyperde3=0.000005
				
			sec.catau_ccanl = 10
			sec.caiinf_ccanl = 5.e-6
			
			sec.enat = 55
			sec.ekf = -90
			sec.ek = -90
			sec.esk=-90
			sec.elca=130
			sec.el_ichan2 =-70.45
			sec.ehyf=-40
			sec.ehys=-40
            sec.Ra = 100

		self.cao_ccanl=2  


    def connect2target(self,target, delay = 1, weight=0.04): # { localobj nc #$o1 target point process, optional $o2 returned NetCon
        self.nc.append(h.NetCon(self.soma(0.5)._ref_v, target, sec=self.soma))
        self.nc[-1].threshold = -10 # mV
        self.nc[-1].delay = delay # ms
        self.nc[-1].weight[0] = weight # NetCon weight is a vector    
        return self.nc[-1]


    def addSynapses(self):
        self.pre_list = []

        # PP(AMPA) syn to dist dend similar to PP to GC
        syn_ = h.Exp2Syn(self.mcdend1[3](0.7))
        self.pre_list.append(syn_)  
        syn_.tau1 = 1.5
        syn_.tau2 = 5.5
        syn_.e = 0
        
        # PP(AMPA) syn to dist dend similar to PP to GC
        syn_ = h.Exp2Syn(self.mcdend2[3](0.7))
        self.pre_list.append(syn_) 
        syn_.tau1 = 1.5
        syn_.tau2 = 5.5
        syn_.e = 0
       
        # PP(AMPA) syn to dist dend similar to PP to GC
        syn_ = h.Exp2Syn(self.mcdend3[3](0.7))
        self.pre_list.append(syn_) 
        syn_.tau1 = 1.5
        syn_.tau2 = 5.5
        syn_.e = 0
       
        # PP(AMPA) syn to dist dend similar to PP to GC
        syn_ = h.Exp2Syn(self.mcdend4[3](0.7))
        self.pre_list.append(syn_) 
        syn_.tau1 = 1.5
        syn_.tau2 = 5.5
        syn_.e = 0
        
        # GC(AMPA) syn to prox dend similar to GC>CA3 Jonas '93
        syn_ = h.Exp2Syn(self.mcdend1[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .5
        syn_.tau2 = 6.2
        syn_.e = 0
        
        # GC(AMPA) syn to prox dend similar to GC>CA3 Jonas '93
        syn_ = h.Exp2Syn(self.mcdend2[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .5
        syn_.tau2 = 6.2
        syn_.e = 0
        
        # GC(AMPA) syn to prox dend similar to GC>CA3 Jonas '93
        syn_ = h.Exp2Syn(self.mcdend3[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .5
        syn_.tau2 = 6.2
        syn_.e = 0
        
         # GC(AMPA) syn to prox dend similar to GC>CA3 Jonas '93
        syn_ = h.Exp2Syn(self.mcdend4[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .5
        syn_.tau2 = 6.2
        syn_.e = 0
        
        #  MC(AMPA) syn to prox dend similar to CA#>CA3 Aaron
        syn_ = h.Exp2Syn(self.mcdend1[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.45
        syn_.tau2 = 2.2
        syn_.e = 0
        
       #  MC(AMPA) syn to prox dend similar to CA#>CA3 Aaron
        syn_ = h.Exp2Syn(self.mcdend2[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.45
        syn_.tau2 = 2.2
        syn_.e = 0
        
        #  MC(AMPA) syn to prox dend similar to CA#>CA3 Aaron
        syn_ = h.Exp2Syn(self.mcdend3[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.45
        syn_.tau2 = 2.2
        syn_.e = 0
     
       #  MC(AMPA) syn to prox dend similar to CA#>CA3 Aaron
        syn_ = h.Exp2Syn(self.mcdend4[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.45
        syn_.tau2 = 2.2
        syn_.e = 0
     
       #  BC(GABA) syn to prox dend based on BC>CA3 Bartos PNAS (mice)
        syn_ = h.Exp2Syn(self.soma(0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.3
        syn_.tau2 = 3.3
        syn_.e = -70
		        
        #  HIPP(GABA) syn to prox dend based on Hilar>GC Harney&Jones
        syn_ = h.Exp2Syn(self.mcdend1[2](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.5
        syn_.tau2 = 6
        syn_.e = -70
		        
        #  HIPP(GABA) syn to prox dend based on Hilar>GC Harney&Jones
        syn_ = h.Exp2Syn(self.mcdend2[2](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.5
        syn_.tau2 = 6
        syn_.e = -70
		        
        #  HIPP(GABA) syn to prox dend based on Hilar>GC Harney&Jones
        syn_ = h.Exp2Syn(self.mcdend3[2](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.5
        syn_.tau2 = 6
        syn_.e = -70
		        
        #  HIPP(GABA) syn to prox dend based on Hilar>GC Harney&Jones
        syn_ = h.Exp2Syn(self.mcdend4[2](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.5
        syn_.tau2 = 6
        syn_.e = -70
		
		# Total of 17 synapses 	0-3 PP; 	4-7 GC; 	8-11 MC; 	12 BC; 	13-16 HIPP 

class HIPPCell(modelcell):
    """ HIPP Cell definition """
    def __init__(self, gid = -1):
        super().__init__()
        self.gid = gid
        self.create_sections() 
        self.build_topology()
        self.build_subsets() # subsets()
        self.define_geometry() # geom()
        self.define_biophysics() # biophys()
        self.addSynapses() # synapses
        
    def __repr__(self):
        return "HIPP Cell {}".format(self.gid)

    def create_sections(self):
        self.soma = h.Section(name='soma', cell=self)
		self.hcdend1 = []
		self.hcdend2 = []
		self.hcdend3 = []
		self.hcdend4 = []
		
		for r in range(3):
			self.hcdend1.append(h.Section(name='hcdend1['+str(r)+']', cell=self))
			self.hcdend2.append(h.Section(name='hcdend2['+str(r)+']', cell=self))
			self.hcdend3.append(h.Section(name='hcdend3['+str(r)+']', cell=self))
			self.hcdend4.append(h.Section(name='hcdend4['+str(r)+']', cell=self))

    def build_topology(self):
        self.hcdend1[0].connect(self.soma(1))
        self.hcdend2[0].connect(self.soma(1))
        self.hcdend3[0].connect(self.soma(0))
        self.hcdend4[0].connect(self.soma(0))
		
		for r in range(1,3):
			self.hcdend1[r].connect(self.hcdend1[r-1](1))
			self.hcdend2[r].connect(self.hcdend2[r-1](1))
			self.hcdend3[r].connect(self.hcdend3[r-1](1))
			self.hcdend4[r].connect(self.hcdend4[r-1](1))
      

    def define_geometry(self):
		self.soma.nseg=1 
		self.soma.L=20 
		self.soma.diam=10
		
		diamlist=[5.78, 4, 2.5, 1]

		for r in range(3):
			self.mcdend1[r].nseg=1 
			self.hcdend1[r].L=75 
			self.hcdend1[r].diam=3-r

			self.hcdend2[r].nseg=1 
			self.hcdend2[r].L=75 
			self.hcdend2[r].diam=3-r

			self.hcdend3[r].nseg=1 
			self.hcdend3[r].L=50 
			self.hcdend3[r].diam=3-r

			self.hcdend4[r].nseg=1 
			self.hcdend4[r].L=50 
			self.hcdend4[r].diam=3-r

    def build_subsets(self):
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

		self.pdend  = h.SectionList()
		self.pdend.append(self.hcdend1[0])
		self.pdend.append(self.hcdend2[0])
		self.pdend.append(self.hcdend3[0])
		self.pdend.append(self.hcdend4[0])

		self.ddend  = h.SectionList()
		for r in range(1,3):
			self.ddend.append(self.hcdend1[r])
			self.ddend.append(self.hcdend2[r])
			self.ddend.append(self.hcdend3[r])
			self.ddend.append(self.hcdend4[r])

    def define_biophysics(self):      
        self.soma.insert("ichan2") # modified from Aradi and Soltesz 2002
		self.soma.cm=0.6
		
        for seg in self.soma:
            seg.gnatbar_ichan2=0.2  
            seg.gkfbar_ichan2=0.006  
            seg.gl_ichan2=0.000036
		self.soma.cm=1.1

        for sec in self.pdend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002
			for seg in sec:
				seg.gnatbar_ichan2=0.2  
				seg.gkfbar_ichan2=0.006  
				seg.gl_ichan2=0.000036		
			sec.cm = 1.1

        for sec in self.ddend:
			sec.insert("ichan2") # modified from Aradi and Soltesz 2002

			for seg in sec:
				seg.gnatbar_ichan2=0.0  
				seg.gkfbar_ichan2=0.00 
				seg.gl_ichan2=0.000036		
			sec.cm = 1.1

        for sec in self.all:
        	sec.insert("borgka") # KA from Aradi and Soltesz 2002
        	sec.insert("nca") # NVA Ca++-L type current
        	sec.insert("lca") # HVA Ca++-L type current
        	sec.insert("gskch") # SK channel from Aradi and Soltesz 2002
        	sec.insert("cagk") # from Migliore et al., 1995
        	sec.insert("hyperde3") # from Migliore et al., 1995
            sec.insert("ccanl")
			for seg in sec:
				seg.gkabar_borgka=0.0008			
				seg.gncabar_nca=0.0			
				seg.glcabar_lca=0.0015		
				seg.gskbar_gskch=0.003
				seg.gkbar_cagk=0.003
				seg.ghyfbar_hyperde3=0.000015
				seg.ghysbar_hyperde3=0.000015
				
			sec.catau_ccanl = 10
			sec.caiinf_ccanl = 5.e-6
			
			sec.enat = 55
			sec.ekf = -90
			sec.ek = -90
			sec.esk=-90
			sec.elca=130
			sec.el_ichan2 =-70.45
			sec.ehyf=-40
			sec.ehys=-40
            sec.Ra = 100

		self.cao_ccanl=2  

		# // CURRENT INJECTION
		# //for i=0,0 {
		# //stimdel[i]=1
		# //stimdur[i]=300
		# //stimamp[i]=0.65 // to reproduce 2-4Hz firing in vitro in the presence of baseline fluctuations
		# //soma stim[i] = new IClamp(0.5)
		# //stim.del[i]=stimdel[i]
		# //stim.dur[i]=stimdur[i]
		# //stim.amp[i]=stimamp[i]
		# //}

		# // FLUCTUATING CONDUCTANCE DESTEXHE ET AL., 2001
		# //objref fl
		# //soma fl = new Gfluct2(0.5)
		# //fl.g_e0 = 0.0242
		# //fl.g_i0 = 0.1146
		# //fl.std_e = 0.0375
		# //fl.std_i = 0.01875           


    def connect2target(self,target, delay = 1, weight=0.04): # { localobj nc #$o1 target point process, optional $o2 returned NetCon
        self.nc.append(h.NetCon(self.soma(0.5)._ref_v, target, sec=self.soma))
        self.nc[-1].threshold = -10 # mV
        self.nc[-1].delay = delay # ms
        self.nc[-1].weight[0] = weight # NetCon weight is a vector    
        return self.nc[-1]


    def addSynapses(self):
        self.pre_list = []

        # GC(AMPA) syn to prox dend similar to GC>BC
        syn_ = h.Exp2Syn(self.hcdend1[0](0.5))
        self.pre_list.append(syn_)  
        syn_.tau1 = 0.3
        syn_.tau2 = 0.6
        syn_.e = 0
        
        # GC(AMPA) syn to prox dend similar to GC>BC
        syn_ = h.Exp2Syn(self.hcdend2[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.3
        syn_.tau2 = 0.6
        syn_.e = 0
       
        # GC(AMPA) syn to prox dend similar to GC>BC
        syn_ = h.Exp2Syn(self.hcdend3[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.3
        syn_.tau2 = 0.6
        syn_.e = 0
       
        # GC(AMPA) syn to prox dend similar to GC>BC
        syn_ = h.Exp2Syn(self.hcdend4[0](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = 0.3
        syn_.tau2 = 0.6
        syn_.e = 0
        
        # MC(AMPA) syn to mid dend similar to CA3>int Aaron
        syn_ = h.Exp2Syn(self.hcdend1[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .9
        syn_.tau2 = 3.6
        syn_.e = -70 # diff than model template I took it from, that seems to be wrong
        
        # MC(AMPA) syn to mid dend similar to CA3>int Aaron
        syn_ = h.Exp2Syn(self.hcdend2[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .9
        syn_.tau2 = 3.6
        syn_.e = -70 # diff than model template I took it from, that seems to be wrong

        # MC(AMPA) syn to mid dend similar to CA3>int Aaron
        syn_ = h.Exp2Syn(self.hcdend3[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .9
        syn_.tau2 = 3.6
        syn_.e = -70 # diff than model template I took it from, that seems to be wrong
        
        # MC(AMPA) syn to mid dend similar to CA3>int Aaron
        syn_ = h.Exp2Syn(self.hcdend4[1](0.5))
        self.pre_list.append(syn_) 
        syn_.tau1 = .9
        syn_.tau2 = 3.6
        syn_.e = -70 # diff than model template I took it from, that seems to be wrong

		# Total of 8 synapses butt Viji's doc says there should be 12...
		# Total of 12 synapses 	0-3 PP; 	4-7 GC; 	8-11 MC	


class PPstim(modelcell):  
    """ Stim cell with stim attribute that references a RegnStim point process """
    def __init__(self, gid=-1):
        super().__init__()
        self.gid = gid

        self.is_art =1
        self.ncstim = []
        self.stim = h.NetStim()
       	self.stim.number = 1
       	self.stim.start = 5
       	self.stim.interval = 100
       	self.stim.noise = 0
           
    def __repr__(self):
        return "Stim cell {}: ISI is {} ms".format(self.gid, self.stim.interval)

    def connect2target(self,target, delay = 1, weight=0.04): # { localobj nc #$o1 target point process, optional $o2 returned NetCon
        self.ncstim.append(h.NetCon(self.stim, target))
        self.ncstim[-1].delay = delay # ms
        self.ncstim[-1].weight[0] = weight # NetCon weight is a vector    
        return self.ncstim[-1]