shader_type spatial;
render_mode diffuse_burley, specular_schlick_ggx;
uniform sampler2D earth_color : source_color, filter_linear_mipmap_anisotropic, repeat_enable;
uniform sampler2D earth_normal : hint_normal, filter_linear_mipmap_anisotropic, repeat_enable;
uniform sampler2D earth_roughness : filter_linear_mipmap_anisotropic, repeat_enable;
varying vec3 world_position;

float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1,311.7))) * 43758.5453); }
float noise(vec2 p) {
	vec2 i=floor(p), f=fract(p); f=f*f*(3.0-2.0*f);
	return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);
}
void vertex() { world_position=(MODEL_MATRIX*vec4(VERTEX,1.0)).xyz; }
void fragment() {
	vec2 p=world_position.xz;
	float macro=noise(p*.17)*.65+noise(p*.43+17.0)*.35;
	vec2 a=p*.58, b=mat2(vec2(.799,.602),vec2(-.602,.799))*p*.91+vec2(7.31,2.47);
	float blend=smoothstep(.28,.72,noise(p*.32));
	vec3 soil=mix(texture(earth_color,a).rgb,texture(earth_color,b).rgb,blend);
	// Broad damp patches follow garden edges; compact soil remains around the path.
	float edge=smoothstep(7.0,13.5,abs(p.x));
	float garden=smoothstep(.42,.73,macro)*mix(.20,.85,edge);
	float anchors=max(exp(-dot(p-vec2(-8,0),p-vec2(-8,0))*.13),exp(-dot(p-vec2(8,-3),p-vec2(8,-3))*.13));
	anchors=max(anchors,exp(-dot(p-vec2(5.8,2),p-vec2(5.8,2))*.38));
	garden=max(garden,anchors*smoothstep(.30,.68,macro)*.78);
	float walked=1.0-smoothstep(1.3,3.1,abs(p.x));
	vec3 dry=soil*mix(vec3(.71,.69,.57),vec3(1.02,.94,.76),macro);
	vec3 damp=mix(soil*.42,vec3(.034,.052,.023),.62);
	ALBEDO=mix(dry,damp,garden)*(1.0+walked*.055);
	ROUGHNESS=clamp(texture(earth_roughness,a).r*.35+.58-garden*.11,.64,.98);
	NORMAL_MAP=texture(earth_normal,a).rgb;
	NORMAL_MAP_DEPTH=.32;
}
