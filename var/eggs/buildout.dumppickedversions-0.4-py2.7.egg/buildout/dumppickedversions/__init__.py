import os
import sys
import logging
import zc.buildout.easy_install
import pkg_resources

logger = zc.buildout.easy_install.logger

required_by = {}

def _log_requirement(ws, req):
    ws = list(ws)
    ws.sort()
    for dist in ws:
        if req in dist.requires():
            req_ = str(req)
            dist_ = str(dist)
            if req_ in required_by and dist_ not in required_by[req_]:
                required_by[req_].append(dist_)
            else:
                required_by[req_] = [dist_]
            logger.debug("  required by %s." % dist)


def enable_dumping_picked_versions(old_get_dist):
    def get_dist(self, requirement, ws, always_unzip):
        dists = old_get_dist(self, requirement, ws, always_unzip)
        for dist in dists:
            if not (dist.precedence == pkg_resources.DEVELOP_DIST or \
                    (len(requirement.specs) == 1 and requirement.specs[0][0] == '==')):
                self.__picked_versions[dist.project_name] = dist.version
        return dists        
    return get_dist


def dump_picked_versions(old_logging_shutdown, file_name, overwrite):

    def logging_shutdown():

        picked_versions_top = '[versions]\n'
        picked_versions_bottom = ''
        for d, v in sorted(zc.buildout.easy_install.Installer.__picked_versions.items()):
            if d in required_by:
                req_ = "\n#Required by:\n#" + "\n#".join(required_by[d]) + "\n"
                picked_versions_bottom += "%s%s = %s\n" % (req_, d, v)
            else:
                picked_versions_top += "%s = %s\n" % (d, v)

        picked_versions = picked_versions_top + picked_versions_bottom

        if file_name is not None:
            if not os.path.exists(file_name):
                print "*********************************************"
                print "Writing picked versions to %s" % file_name
                print "*********************************************"
                open(file_name, 'w').write(picked_versions)
            elif overwrite:
                print "*********************************************"
                print "Overwriting %s" % file_name
                print "*********************************************"
                open(file_name, 'w').write(picked_versions)
            else:    
                print "*********************************************"
                print "Skipped: File %s already exists." % file_name                 
                print "*********************************************"
        else:
            print "*************** PICKED VERSIONS ****************"
            print picked_versions
            print "*************** /PICKED VERSIONS ***************"

        old_logging_shutdown()    
    return logging_shutdown


def install(buildout):

    file_name = 'dump-picked-versions-file' in buildout['buildout'] and \
                buildout['buildout']['dump-picked-versions-file'].strip() or \
                None
                
    overwrite = 'overwrite-picked-versions-file' not in buildout['buildout'] or \
                buildout['buildout']['overwrite-picked-versions-file'].lower() \
                in ['yes', 'true', 'on']

    zc.buildout.easy_install.Installer.__picked_versions = {}
    zc.buildout.easy_install._log_requirement = _log_requirement
    zc.buildout.easy_install.Installer._get_dist = enable_dumping_picked_versions(
                                  zc.buildout.easy_install.Installer._get_dist)
    
    logging.shutdown = dump_picked_versions(logging.shutdown, 
                                            file_name, 
                                            overwrite)
    
