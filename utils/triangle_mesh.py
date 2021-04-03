import numpy as np

def clean_doubled_faces(trimesh):
    faces_o = np.sort(trimesh.triangles)
    _, idx = np.unique(faces_o, axis=0, return_index=True)

    mask = np.ones(len(faces_o), dtype=int)
    mask[idx]=0
    trimesh.remove_triangles_by_mask(mask)

def clean_doubled_faces2(faces):
    faces_o = np.sort(faces)
    _, idx = np.unique(faces_o, axis=0, return_index=True)
    return faces[idx]

def normalize_v3(arr):
    ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
    lens = np.sqrt( arr[:,0]**2 + arr[:,1]**2 + arr[:,2]**2 )
    arr[:, 0] /= lens
    arr[:, 1] /= lens
    arr[:, 2] /= lens
    return arr

def calc_normals(triangle_mesh, v_normals=True, output_numpy=True, as_array=False):
    if as_array:
        np_verts, np_faces = triangle_mesh
    else:
        np_verts = np.asarray(triangle_mesh.vertices)
        np_faces = np.asarray(triangle_mesh.triangles)
    if v_normals:
        norm = np.zeros(np_verts.shape, dtype=np_verts.dtype)
    v_pols = np_verts[np_faces]
    face_normals = np.cross( v_pols[::,1 ] - v_pols[::,0]  , v_pols[::,2 ] - v_pols[::,0] )
    normalize_v3(face_normals)
    if v_normals:
        for i in range(np_faces.shape[1]):
            norm[ np_faces[:,i] ] += face_normals
    if v_normals:
        if output_numpy:
            return face_normals, normalize_v3(norm)
        else:
            return face_normals.tolist(), normalize_v3(norm).tolist()
    else:
        return face_normals if output_numpy else  face_normals.tolist()

def calc_centers(triangle_mesh, output_numpy=True):

    np_verts = np.asarray(triangle_mesh.vertices)
    np_faces = np.asarray(triangle_mesh.triangles)
    v_pols = np_verts[np_faces]
    center = np.sum(v_pols,axis=1)/3

    return center if output_numpy else  center.tolist()

def calc_mesh_tris_areas(mesh, output_numpy=True):
    if output_numpy:
        return calc_tris_areas(np.asarray(mesh.vertices)[np.asarray(mesh.triangles)])
    return calc_tris_areas(np.asarray(mesh.vertices)[np.asarray(mesh.triangles)]).tolist()
    

def calc_tris_areas(v_pols):
    perp = np.cross(v_pols[:, 1]- v_pols[:, 0], v_pols[:, 2]- v_pols[:,0])/2
    return np.linalg.norm(perp, axis=1)/2
